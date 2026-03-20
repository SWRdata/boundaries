<script>
  import { dev } from "$app/environment";

  import {
    Map,
    SWRDataLabLight,
    VectorTileSource,
    VectorLayer,
    NavigationControl,
    Tooltip,
    tokens,
    AttributionControl,
  } from "@swr-data-lab/components";

  import Sidebar from "./Sidebar.svelte";

  const { timestamps = [] } = $props();

  const levels = [2, 4, 6, 8];
  const labels = ["Default", "None"];

  let filter = $state(levels[1]);
  let date = $state(timestamps[timestamps.length - 1]);
  let showLabels = $state(labels[0]);

  let tileUrls = $derived(
    false
      ? [
          [
            "boundaries",
            `http://localhost:8080/tiles/admin_boundaries/tiles.json`,
          ],
          ["labels", `http://localhost:8080/tiles/admin_labels/tiles.json`],
        ]
      : [
          [
            "boundaries",
            `https://static.datenhub.net/data/boundaries/admin_boundaries_${date}.versatiles?{z}/{x}/{y}`,
          ],
          [
            "labels",
            `https://static.datenhub.net/data/boundaries/admin_labels_${date}.versatiles?{z}/{x}/{y}`,
          ],
        ],
  );

  let hoverCoords = $state([]);
  let hovered = $state();
  let tooltipCoordinates = $derived(hovered ? hoverCoords : [0, 0]);

  let fills = [];
  for (let i = 0; i <= 16; i++) {
    const key = Object.keys(tokens.shades)[
      i % Object.keys(tokens.shades).length
    ];
    fills.push(tokens.shades[key].base);
  }

  const handleMouseMove = (e) => {
    hovered = e.features[0];
    hoverCoords = e.lngLat;
  };
  const handleMouseLeave = () => {
    hovered = null;
  };
</script>

<main class="container">
  <Sidebar
    {labels}
    {levels}
    {timestamps}
    bind:date
    bind:filter
    bind:showLabels
  />
  <Map
    initialBounds={[5.86625, 47.270124, 15.041816, 55.058778]}
    initialLocation={{ zoom: 5.9 }}
    style={SWRDataLabLight({
      admin: { show: false, showLabels: false },
      places: { showLabels: false },
    })}
    cursor={hovered ? "pointer" : ""}
    projection={{ type: "globe" }}
    showDebug={dev}
  >
    {#each tileUrls as [id, url]}
      {#if url.includes("tiles.json")}
        <VectorTileSource {id} {url} />
      {:else}
        <VectorTileSource
          {id}
          tiles={[url]}
          maxZoom={8}
          attribution={`© BKG ${date.replace("-01-01", "")} dl-de/by-2-0`}
        />
      {/if}
    {/each}

    <VectorLayer
      id="admin-fill"
      type="fill"
      sourceId="boundaries"
      sourceLayer="administrative"
      placeBelow=""
      filter={["==", "admin_level", filter]}
      onmouseleave={handleMouseLeave}
      onmousemove={handleMouseMove}
      paint={{
        "fill-color": [
          "match",
          ["get", "land"],
          ...fills
            .map((v, i) => {
              return [`${i + 1}`.padStart(2, "0"), v];
            })
            .flat(),
          tokens.shades.blue.light4,
        ],
        "fill-opacity": 0.125,
      }}
    />
    <VectorLayer
      bind:hovered
      id="outline"
      sourceId="boundaries"
      sourceLayer="administrative"
      type="line"
      filter={["==", "admin_level", filter]}
      paint={{
        "line-width": 0.75,
        "line-color": tokens.shades.gray.base,
        "line-opacity": 1,
      }}
    />

    <VectorLayer
      id="outline-state"
      sourceId="boundaries"
      sourceLayer="administrative"
      type="line"
      filter={["==", "admin_level", 2]}
      paint={{
        "line-width": 1.5,
        "line-color": tokens.shades.gray.dark2,
        "line-opacity": 1,
      }}
    />

    <VectorLayer
      bind:hovered
      id="outline-hover"
      sourceId="boundaries"
      sourceLayer="administrative"
      type="line"
      filter={["==", "admin_level", filter]}
      paint={{
        "line-width": [
          "case",
          ["any", ["boolean", ["feature-state", "hovered"], false]],
          1.75,
          0,
        ],
        "line-color": "black",
        "line-opacity": 1,
      }}
    />

    {#if showLabels !== "None"}
      <VectorLayer
        id="labels-state"
        sourceId="labels"
        sourceLayer="administrative"
        type="symbol"
        filter={["==", "admin_level", filter]}
        layout={{
          "text-size": 16,
          "text-max-width": 5,
          "text-font": ["swr_sans_medium"],
          "text-field": "{name}",
        }}
        paint={{
          "text-halo-color": "rgba(255,255,255,.95)",
          "text-halo-width": 1.5,
          "text-halo-blur": 2,
          "text-color": "black",
        }}
      />
    {/if}

    {#if hovered}
      <Tooltip
        position={tooltipCoordinates}
        mouseEvents={false}
        showCloseButton={false}
        closeOnClick={false}
      >
        <table class="tooltip-body">
          <tbody>
            {#each Object.entries(hovered.properties) as [k, v]}
              <tr><th>{k}</th><td>{v}</td></tr>
            {/each}
          </tbody>
        </table>
      </Tooltip>
    {/if}

    <AttributionControl position="bottom-left" />
    <NavigationControl position="bottom-right" />
  </Map>
</main>

<style lang="scss">
  .container {
    width: 100%;
    flex-grow: 1;
    height: 100%;
    height: 100vh;
    position: relative;
    font-family: var(--swr-sans);
  }

  .tooltip-body {
    font-family: monospace;
    border-spacing: 0;
    font-size: 0.75rem;
    text-align: left;
    th {
      color: var(--blue-base);
      font-weight: normal;
    }
    td,
    th {
      border-bottom: 1px solid lightgray;
      padding: 0.15em 0;
      padding-right: 1.5em;
      &:last-child {
        padding-right: 0;
      }
    }
    tr:last-child {
      td,
      th {
        border-bottom: 0;
        padding-bottom: 0;
      }
    }
  }
</style>
