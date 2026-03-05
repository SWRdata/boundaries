<script>
  let { date, dates, filter, levels } = $props();

  const usage = `
map.addSource("boundaries", {
    type: "vector",
    url: "https://tiles.datenhub.net/tiles/boundaries/tiles.json"
});`
</script>

<div class="container">
  <span class="eyebrow">SWR Data Lab</span>
  <h1>Boundaries</h1>

  <form>
    <div class="input">
      <label for="date-select">Stand</label>
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

  <details open>
    <summary>Usage</summary>
    <code>
    <pre>{usage.trim()}</pre>
</code>
  </details>
  <p class="footer">
    <a href="#1">Github</a>
  </p>
</div>

<style lang="scss">
  .eyebrow {
    font-size: var(--fs-small-3);
    display: block;
  }
  h1 {
    font-weight: 700;
    font-size: var(--fs-large-1);
    margin-bottom: 0.5em;
  }
  .container {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    right: .5rem;
    max-width: 20em;
    z-index: 100;
    background: var(--color-pageFill);
    padding: 0.75rem;
    border-radius: 3px;
    padding-right: 1.25rem;
    box-shadow: 0px 1px 3px rgba(black, 0.1);
    border: 1px solid rgba(black, 0.75);
  }
  form {
    display: flex;
    gap: 0.5em;
    margin-bottom: .5em;;
  }
  select {
    background: transparent;
    padding: 0.2rem 0.45rem;
    border: 1px solid var(--gray-light-1);
    border-radius: 2px;
  }
  pre {
    overflow-x: scroll;
    border: 1px solid var(--gray-light-1);
    padding: .5em;
  }
  code {
    font-family: monospace;
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
  .footer {
    font-size: var(--fs-small-3);
    margin-top: 1.5em;
    color: var(--gray-dark-1);
    a {
      text-decoration: none;
    }
  }
</style>
