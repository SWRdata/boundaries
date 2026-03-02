<script>
	import { dev } from '$app/environment'

	import { Map, SWRDataLabLight, VectorTileSource, VectorLayer, NavigationControl, Tooltip, AttributionControl } from '@swr-data-lab/components'

	// 1. Set config variables
	// Cache busting using Date.now(), see: https://github.com/mapbox/mapbox-gl-js/issues/2633#issuecomment-516705491
	const tileUrls = false
		? {
				rent: `http://127.0.0.1:8080/tiles/rent/{z}/{x}/{y}?dt=${Date.now()}`,
				admin: `http://127.0.0.1:8080/tiles/admin/{z}/{x}/{y}?dt=${Date.now()}`,
			}
		: {
				rent: `https://static.datenhub.net/data/p109_besser_wohnen/rent_merged_4.versatiles?{z}/{x}/{y}`,
				admin: `https://static.datenhub.net/data/p109_besser_wohnen/admin_boundaries.versatiles?{z}/{x}/{y}`,
			}

	let tooltipCoordinates = $derived(selected ? selectionCoordinates : [0, 0])
	let tooltipData = $derived(selected?.properties)
	let hovered = $state(null)

	const handleMouseMove = (e) => {
		hovered = e.features?.[0]
	}
	const handleMouseLeave = (e) => {
		hovered = null
	}
</script>

<figure class="container">
	<Map initialBounds={[5.87, 46.85, 15.04, 55.4]} minZoom={4} style={SWRDataLabLight({ places: { showLabels: false } })} cursor={hovered ? 'pointer' : ''} projection={{ type: 'globe' }} showDebug={false}>
		<!-- <VectorTileSource id="admin_boundaries" url={tileUrls['admin']} minZoom={4} maxZoom={14.99} /> -->

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
