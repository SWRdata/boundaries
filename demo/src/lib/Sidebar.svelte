<script>
	import Highlight, { HighlightSvelte } from 'svelte-highlight'
	import typescript from 'svelte-highlight/languages/typescript'
	import githubStyle from 'svelte-highlight/styles/github'

	let { date, dates, filter, levels } = $props()

	const usages = $derived({
		Javascript: `
const map = new maplibregl.Map({
    container: 'map',
    style: 'https://tiles.openfreemap.org/styles/bright',
    zoom: 13,
    center: [50, 9]
});

map.on("load", () => {
  map.addSource("boundaries", {
    type: "vector",
    tiles: ["https://tiles.datenhub.net/tiles/boundaries/{z}/{x}/{y}"]
    attribution: "© BKG (${date.slice(0, 4)}) dl-de/by-2-0"
  });
  map.addLayer({
    id: "states",
    type: "line",
    source: "boundaries",
    sourceLayer: "administrative"
    filter: ["==", "admin_level", ${filter}]
    paint: {"line-color": "red"}
  });
})
`,
		'Data Lab Components (Svelte)': `
<Map style={SWRDataLabLight()}>
  <VectorTileSource
    id="boundaries"
    url="https://tiles.datenhub.net/tiles/boundaries/tiles.json">
  </VectorTileSource>
  <VectorLayer
    type="line"
    id="states"
    sourceId="boundaries"
    sourceLayer="administrative"
    filter={["==", "admin_level", ${filter}]}
    paint={{"line-color": "red"}}
  ></VectorLayer>
</Map>
`,
	})
</script>

<svelte:head>
	{@html githubStyle}
</svelte:head>

<div class="container">
	<span class="eyebrow">SWR Data Lab</span>
	<h1>Boundaries</h1>

	<form>
		<div class="input">
			<label for="date-select">Date</label>
			<select name="date-select" id="" bind:value={date}>
				{#each dates as d}
					<option value={d}>{d}</option>
				{/each}
			</select>
		</div>
		<div class="input">
			<label for="level-select">Admin level</label>
			<select name="level-select" id="" bind:value={filter}>
				{#each levels as l}
					<option value={l}>{l}</option>
				{/each}
			</select>
		</div>
	</form>

	<h2>Usage</h2>
	<ul class="usages">
		{#each Object.entries(usages) as [key, value], i}
			{@const code = value.trim()}
			<li>
				<details open={i === 0}>
					<summary>{key}</summary>
					<div class="code">
						{#if key.includes('Components')}
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
		<a href="https://github.com/SWRdata/boundaries">Docs</a>
		<a href="https://github.com/SWRdata/components">Data Lab Components</a>
		<span>© {new Date().getFullYear()}</span>
	</p>
</div>

<style lang="scss">
	.container {
		position: absolute;
		top: 0.5rem;
		left: 0.5rem;
		right: 0.5rem;
		max-width: 20em;
		z-index: 100;
		background: var(--color-pageFill);
		padding: 0.75rem;
		border-radius: 3px;
		padding-right: 1.25rem;
		box-shadow: 0px 1px 3px rgba(black, 0.1);
		border: 1px solid rgba(black, 0.75);
	}

	.eyebrow {
		font-size: var(--fs-small-3);
		display: block;
	}
	h1 {
		font-weight: 700;
		font-size: var(--fs-large-2);
		margin-bottom: 0.5em;
	}

	form {
		display: flex;
		gap: 0.5em;
		margin-bottom: 1em;
	}
	select {
		background: transparent;
		padding: 0.2rem 0.45rem;
		border: 1px solid var(--gray-light-1);
		border-radius: 2px;
	}

	label {
		display: block;
		font-size: var(--fs-small-3);
		margin-bottom: 0.1em;
	}
	select {
		font-size: var(--fs-small-2);
	}
	.input {
		display: flex;
		flex-basis: 0;
		flex-grow: 1;
		flex-flow: column;
		gap: 0.2em;
	}
	.usages {
		display: flex;
		flex-flow: column;
		list-style: none;
		li {
			border-bottom: 1px solid var(--gray-light-2);
		}
	}
	summary {
		font-size: var(--fs-small-2);
		padding: 0.5em 0;
		cursor: pointer;
		user-select: none;
	}

	.code {
		border: 1px solid var(--gray-light-1);
		font-family: monospace;
	}
	:global(code) {
		scrollbar-width: thin;
	}
	.footer {
		font-size: var(--fs-small-3);
		margin-top: 1em;
		color: var(--gray-dark-1);
		display: flex;
		gap: 1em;
		align-items: baseline;
		a {
			text-decoration: none;
			color: var(--blue-dark-3);
			&:hover,
			&:focus-visible {
				text-decoration: underline;
			}
		}
	}
</style>
