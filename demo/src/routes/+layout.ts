import type { LayoutServerLoad } from "./$types";
export const prerender = true;

export const load: LayoutServerLoad = async ({ fetch }) => {
  const res = await fetch(
    "https://static.datenhub.net/data/boundaries/manifest.csv",
  );

  let timestamps: string[] = [];

  if (res.ok) {
    const text = await res.text();
    timestamps = Array.from(
      new Set(
        text
          .split("\n")
          .slice(1)
          .map((f: string) => {
            const m = f.match(/(?:.+_)(\d+-\d+-\d+)(?:.+)/);
            return m ? m[1] : null;
          })
          .filter((f: string | null): f is string => f !== null),
      ),
    ).sort((a, b) => b.localeCompare(a));
  }

  return { timestamps };
};
