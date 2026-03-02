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

  const tileUrl = dev
    ? `http://127.0.0.1:8080/tiles/boundaries/{z}/{x}/{y}?dt=${Date.now()}`
    : `https://static.datenhub.net/data/p109_besser_wohnen/admin_boundaries.versatiles?{z}/{x}/{y}`;

  let hoverCoords = $state([]);

  let tooltipCoordinates = $derived(hovered ? hoverCoords : [0, 0]);
  let tooltipData = $derived(selected?.properties);

  let hovered = $state();

  const handleMouseMove = (e) => {
    hovered = e.features[0];
    hoverCoords = e.lngLat;
  };
  const handleMouseLeave = (e) => {
    console.log(hovered);
    hovered = null;
  };
  let filter = $state("land");
</script>

<figure class="container">
  <div class="controls">
    <h1>SWRDL Boundaries</h1>
    <div class="input">
      <label for="level-select">Level</label>
      <select name="level-select" id="" bind:value={filter}>
        <option value="staat">Staat</option>
        <option value="land">Bundesländer</option>
        <option value="kreis">Kreise</option>
        <option value="gemeinde">Gemeinden</option>
      </select>
    </div>
  </div>
  <Map
    initialBounds={[5.87, 46.85, 15.04, 55.4]}
    minZoom={4}
    style={SWRDataLabLight({
      admin: { show: false },
    })}
    cursor={hovered ? "pointer" : ""}
    projection={{ type: "globe" }}
    showDebug
  >
    <VectorTileSource id="boundaries" url={tileUrl} />

    <VectorLayer
      id="fill"
      sourceId="boundaries"
      sourceLayer="boundaries"
      type="fill"
      filter={["==", "kind", filter]}
      onmouseleave={handleMouseLeave}
      onmousemove={handleMouseMove}
      paint={{
        "fill-color": [
          "match",
          ["get", "ARS"],
          "01",
          tokens.shades.forest.light3,
          "02",
          tokens.shades.forest.light1,
          "03",
          tokens.shades.teal.light1,
          tokens.shades.blue.light3,
        ],
        "fill-opacity": 0.2,
      }}
    />
    <VectorLayer
      bind:hovered
      id="outline"
      sourceId="boundaries"
      sourceLayer="boundaries"
      type="line"
      filter={["==", "kind", filter]}
      paint={{
        "line-width": [
          "case",
          ["any", ["boolean", ["feature-state", "hovered"], false]],
          1.5,
          0.75,
        ],
        "line-color": "black",
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
</figure>

<style lang="scss">
  .container {
    width: 100%;
    flex-grow: 1;
    height: 100%;
    height: 100vh;
    position: relative;
    font-family: var(--swr-sans);
  }
  h1 {
    font-weight: 600;
    font-size: var(--fs-small-1);
    margin-bottom: 0.25em;
  }
  .controls {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    z-index: 100;
    background: var(--color-pageFill);
    padding: 0.75rem;
    border-radius: 3px;
    padding-right: 1.25rem;
    box-shadow: 0px 1px 3px rgba(black, 0.1);
    border: 1px solid rgba(black, 0.75);
  }
  select {
    background: transparent;
    padding: 0.15rem 0.4rem;
    border: 1px solid gray;
    border-radius: 2px;
  }
  label {
    display: block;
    font-size: var(--fs-small-3);
  }
  select {
    font-size: var(--fs-small-2);
  }
  .input {
    display: flex;
    flex-flow: column;
    gap: 0.2em;
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
