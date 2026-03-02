<script>
  import { dev } from "$app/environment";

  import {
    Map,
    SWRDataLabLight,
    VectorTileSource,
    VectorLayer,
    NavigationControl,
    Tooltip,
    FormLabel,
    AttributionControl,
  } from "@swr-data-lab/components";

  const tileUrl = dev
    ? `http://127.0.0.1:8080/tiles/boundaries/{z}/{x}/{y}?dt=${Date.now()}`
    : `https://static.datenhub.net/data/p109_besser_wohnen/admin_boundaries.versatiles?{z}/{x}/{y}`;

  let tooltipCoordinates = $derived(selected ? selectionCoordinates : [0, 0]);
  let tooltipData = $derived(selected?.properties);

  let hovered = $state();

  const handleMouseMove = (e) => {
    hovered = e.features[0];
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
        "fill-color": "purple",
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
    margin-bottom: 0.5em;
  }
  .controls {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    z-index: 100;
    background: var(--color-pageFill);
    padding: 0.5rem;
    border: 1px solid black;
  }
  label {
    display: block;
    font-size: var(--fs-small-2);
  }
  select {
    font-size: var(--fs-small-2);
  }
  .input {
    display: flex;
    flex-flow: column;
    gap: 0.2em;
  }
</style>
