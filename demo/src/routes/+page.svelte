<script lang="ts">
  import { DesignTokens } from "@swr-data-lab/components";
  import App from "$lib/App.svelte";
  import siteData from "$lib/site.json";

  import screenshot from "$lib/assets/screenshot.png";

  import { page } from "$app/state";
</script>

<svelte:head>
  <title>{siteData.title}</title>
  <meta name="description" content={siteData.description} />

  <meta property="og:url" content="https://www.maxkohler.com/" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content={siteData.title} />
  <meta property="og:description" content={siteData.description} />
  <meta property="og:image" content={screenshot} />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content={siteData.title} />
  <meta name="twitter:description" content={siteData.description} />
  <meta name="twitter:image" content={screenshot} />
</svelte:head>

<DesignTokens theme="light">
  <App timestamps={page.data.timestamps} />
</DesignTokens>
