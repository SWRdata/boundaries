<script>
  import { dev } from "$app/environment";

  import {
    Map,
    SWRDataLabLight,
    VectorTileSource,
    VectorLayer,
    NavigationControl,
    Tooltip,
    AttributionControl,
  } from "@swr-data-lab/components";

  const tileUrl = dev
    ? `http://127.0.0.1:8080/tiles/boundaries/{z}/{x}/{y}?dt=${Date.now()}`
    : `https://static.datenhub.net/data/p109_besser_wohnen/admin_boundaries.versatiles?{z}/{x}/{y}`;

  let tooltipCoordinates = $derived(selected ? selectionCoordinates : [0, 0]);
  let tooltipData = $derived(selected?.properties);
  let hovered = $state(null);

  const handleMouseMove = (e) => {
    hovered = e.features?.[0];
  };
  const handleMouseLeave = (e) => {
    hovered = null;
  };
</script>

<figure class="container">
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
      sourceId="boundaries"
      sourceLayer="boundaries"
      id="outline"
      type="line"
      paint={{
        "line-width": 1,
        "line-color": "purple",
        "line-opacity": 1,
      }}
    />
    <AttributionControl position="bottom-left" />
    <NavigationControl position="top-right" />
  </Map>
</figure>

<style lang="scss">
  .container {
    width: 100%;
    flex-grow: 1;
    height: 100%;
    position: relative;
    height: 100vh;
  }
</style>
