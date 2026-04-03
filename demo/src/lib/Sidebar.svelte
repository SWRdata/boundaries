<script>
  import Highlight, { HighlightSvelte } from "svelte-highlight";
  import typescript from "svelte-highlight/languages/typescript";
  import githubStyle from "svelte-highlight/styles/github";
  import siteData from "$lib/site.json";

  let {
    date = $bindable(),
    timestamps,
    filter = $bindable(),
    showLabels = $bindable(),
    levels,
    labels,
  } = $props();

  const boundaries_url = $derived(
    `https://static.datenhub.net/data/boundaries/admin_boundaries_${date}.versatiles?{z}/{x}/{y}`,
  );
  const labels_url = $derived(
    `https://static.datenhub.net/data/boundaries/admin_labels_${date}.versatiles?{z}/{x}/{y}`,
  );
  const attribution = $derived(
    date ? `© BKG (${date.slice(0, 4)}) dl-de/by-2-0` : "",
  );

  const usages = $derived({
    "Javascript/Maplibre": `
const map = new maplibregl.Map({
    container: 'map',
    style: 'https://tiles.openfreemap.org/styles/bright',
    center: [50, 9],
    zoom: 13
});

map.on("load", () => {
  map.addSource("admin_boundaries", {
    type: "vector",
    tiles: ["${boundaries_url}"],
    attribution: "${attribution}"
  });${
    showLabels !== "None"
      ? `
  map.addSource("admin_labels", {
      type: "vector",
      tiles: ["${labels_url}"],
      attribution: "${attribution}"
  });`
      : ""
  }
  map.addLayer({
    id: "boundaries",
    type: "line",
    source: "admin_boundaries",
    filter: ["==", "admin_level", ${filter}],
    paint: {"line-color": "red"}
  });
  ${
    showLabels !== "None"
      ? `map.addLayer({
    id: "labels",
    type: "symbol",
    source: "admin_labels",
    filter: ["==", "admin_level", ${filter}],
    layout: {'text-field': '{name}'}
  });`
      : ""
  }
})
`,
    "SWRData/components": `
<Map style={SWRDataLabLight()}>
  <VectorTileSource id="admin_boundaries" tiles={["${boundaries_url}"]} attribution="${attribution}"/>${
    showLabels !== "None"
      ? `
  <VectorTileSource id="admin_labels" tiles={["${labels_url}"]} attribution="${attribution}"/>`
      : ""
  }
  <VectorLayer
    type="line"
    id="boundaries"
    sourceId="admin_boundaries"
    sourceLayer="administrative"
    filter={["==", "admin_level", ${filter}]}
    paint={{"line-color": "red"}}
  />
  ${
    showLabels !== "None"
      ? `<VectorLayer
    type="symbol"
    id="labels"
    sourceId="admin_labels"
    sourceLayer="administrative"
    filter={["==", "admin_level", ${filter}]}
    layout={{'text-field': '{name}'}}
  />`
      : ""
  }
</Map>
`,
  });
</script>

<svelte:head>
  {@html githubStyle}
</svelte:head>

<div class="container">
  <header class="header">
    <span class="eyebrow">SWR Data Lab</span>
    <h1>Boundaries</h1>
    <p class="intro">{siteData.description}</p>

    <form>
      <div class="input">
        <label for="date-select">Date</label>
        <select name="date-select" bind:value={date}>
          {#each timestamps as t}
            <option value={t}>{t}</option>
          {/each}
        </select>
      </div>
      <div class="input">
        <label for="level-select">Admin level</label>
        <select name="level-select" bind:value={filter}>
          {#each levels as l}
            <option value={l}>{l}</option>
          {/each}
        </select>
      </div>
      <div class="input">
        <label for="labels-select">Labels</label>
        <select name="labels-select" bind:value={showLabels}>
          {#each labels as l}
            <option value={l}>{l}</option>
          {/each}
        </select>
      </div>
    </form>
  </header>
  <p class="url-label">Tile URL</p>
  <input
    class="link"
    value={`https://static.datenhub.net/data/boundaries/admin_boundaries_${date}.versatiles?{z}/{x}/{y}`}
  />
  <ul class="usages">
    {#each Object.entries(usages) as [key, value], i}
      {@const code = value.trim()}
      <li>
        <details>
          <summary>{key}</summary>
          <div class="code">
            {#if key.includes("Components")}
              <HighlightSvelte {code}></HighlightSvelte>
            {:else}
              <Highlight language={typescript} {code}></Highlight>
            {/if}
          </div>
        </details>
      </li>
    {/each}
  </ul>
  <p class="footer">
    <a href="https://github.com/SWRdata/boundaries">Github</a>
    <span>© {new Date().getFullYear()}</span>
  </p>
</div>

<style lang="scss">
  .container {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    right: 0.5rem;
    max-width: 22em;
    z-index: 100;
    background: var(--color-pageFill);
    padding: 0.85rem;
    border-radius: 3px;
    padding-right: 1.25rem;
    box-shadow: 0px 1px 3px rgba(black, 0.1);
    border: 1px solid rgba(black, 0.75);
  }

  .header {
    padding-bottom: 0.5em;
  }

  .eyebrow {
    font-size: calc(var(--fs-small-3) * 0.9);
    text-transform: uppercase;
    display: block;
    letter-spacing: 0.05em;
  }

  h1 {
    font-weight: 700;
    font-size: var(--fs-large-2);
  }

  .intro {
    margin-bottom: 1.5em;
  }

  form {
    display: flex;
    gap: 0.75em;
    margin-bottom: 0.5em;
  }
  select {
    background: transparent;
    padding: 0.2rem 0.45rem;
    border: 1px solid var(--gray-light-1);
    border-radius: 2px;
    width: 100%;
    font-size: var(--fs-small-2);
  }

  label {
    display: block;
    font-size: var(--fs-small-3);
    margin-bottom: 0.1em;
  }

  .url-label {
    font-size: var(--fs-small-2);
    margin-bottom: 0.25em;
  }

  .input {
    display: flex;
    flex-flow: column;
    gap: 0.2em;
    flex-basis: 0;
    flex-grow: 1;
    align-items: flex-start;
  }

  .usages {
    display: flex;
    flex-flow: column;
    list-style: none;
    li {
      border-bottom: 1px solid var(--gray-light-2);
      &:has([open]) {
        border-bottom: 0;
      }
    }
  }

  summary {
    font-size: var(--fs-small-2);
    padding: 0.5em 0;
    cursor: pointer;
    user-select: none;
  }

  .code {
    font-size: 0.9em;
    border: 1px solid var(--gray-light-2);
    font-family: monospace;
  }

  .link {
    display: block;
    white-space: nowrap;
    padding: 0.4em 0.5em;
    margin-bottom: 0.2em;
    scrollbar-width: none;
    overflow: auto;
    border: 1px solid transparent;
    width: 100%;
    font-family: monospace;
    background: #f7f7f7;
    &:focus {
      outline: none;
      border: 1px solid var(--gray-dark-1);
    }
  }
  :global(code) {
    scrollbar-width: thin;
  }
  .footer {
    font-size: var(--fs-small-3);
    margin-top: 1em;
    color: var(--gray-dark-1);
    display: flex;
    gap: 0.75em;
    align-items: baseline;
    a {
      text-decoration: none;
      color: var(--gray-dark-4);
      &:hover,
      &:focus-visible {
        text-decoration: underline;
      }
    }
  }
</style>
