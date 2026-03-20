import { type PageLoad } from "./$types";
export const prerender = true;

export const load: PageLoad = async ({ fetch }) => {
  const res = await fetch(
    "https://static.datenhub.net/data/boundaries/manifest.csv",
  );

  let files = await res.text();

  const timestamps = Array.from(
    new Set(
      files
        .split("\n")
        .slice(1)
        .map((f: string) => {
          const m = f.match(/(?:.+_)(\d+-\d+-\d+)(?:.+)/);
          return m ? m[1] : null;
        })
        .filter((f: string | null) => {
          return f !== null;
        }),
    ),
  );

  return { timestamps };
};
