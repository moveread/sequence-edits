import { sortBy, prop, range } from 'ramda'

export type Edit = {
  tag: 'insert' | 'skip',
  idx: number
}

export function* decompress(edits: Edit[], n: number): Iterable<number|null> {
  let i = 0;
  for (const { idx, tag } of sortBy(prop('idx'), edits)) {
    yield* range(i, idx);
    if (tag === 'skip')
      i = idx + 1;
    else if (tag === 'insert') {
      yield null;
      i = idx;
    }
  }
  yield* range(i, n)
}

export function* apply<T>(edits: Edit[], xs: T[]): Iterable<T | null> {
  const n = xs.length
  for (const idx of decompress(edits, n)) {
    if (idx === null) {
      yield null
    } else {
      yield xs[idx]
    }
  }
}