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

  const tileUrl = dev
    ? `http://localhost:8080/tiles/boundaries/tiles.json`
    : // `http://localhost:8080/tiles/boundaries/{z}/{x}/{y}?dt=${Date.now()}`
      `https://static.datenhub.net/data/boundaries/boundaries_2025_01-01.versatiles?{z}/{x}/{y}?dt=${Date.now()}`;

  const levels = [2, 4, 6, 8];
  const dates = ["2024-01-01", "2025-01-01"];

  let filter = $state(levels[2]);
  let date = $state(dates[dates.length - 1]);
  let hoverCoords = $state([]);
  let hovered = $state();
  let tooltipCoordinates = $derived(hovered ? hoverCoords : [0, 0]);

  let fills = [];
  for (let i = 0; i < 15; i++) {
    const key = Object.keys(tokens.shades)[
      i % Object.keys(tokens.shades).length
    ];
    fills.push(tokens.shades[key].light1);
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
  <Sidebar {date} {dates} {filter} {levels} />
  <Map
    initialBounds={[5.86625, 47.270124, 15.041816, 55.058778]}
    initialLocation={{ zoom: 5.4 }}
    style={SWRDataLabLight({
      admin: { show: false },
    })}
    cursor={hovered ? "pointer" : ""}
    projection={{ type: "globe" }}
    showDebug
  >
    <VectorTileSource id="boundaries" url={tileUrl} maxzoom={15} />
    <VectorLayer
      id="fill"
      sourceId="boundaries"
      sourceLayer="administrative"
      type="fill"
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
        "fill-opacity": 0.25,
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
        "line-width": [
          "case",
          ["any", ["boolean", ["feature-state", "hovered"], false]],
          1.75,
          0.75,
        ],
        "line-color": [
          "case",
          ["any", ["boolean", ["feature-state", "hovered"], false]],
          "black",
          tokens.shades.gray.base,
        ],
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
              <tr><th>{k}</th><td>{v}</td></tr>{/each}
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
