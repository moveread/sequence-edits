import { sortBy, prop, range } from 'ramda'

export type Edit = {
    type: "insert" | "skip",
    idx: number
}

export function* decompress(edits: Edit[], n: number): Iterable<number|null> {
    let i = 0;
    for (const { idx, type } of sortBy(prop("idx"), edits)) {
        yield* range(i, idx);
        if (type === "skip")
            i = idx + 1;
        else if (type === "insert") {
            yield null;
            i = idx;
        }
    }
    yield* range(i, n)
}