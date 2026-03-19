<script>
	import { DesignTokens } from '@swr-data-lab/components'
	import App from '$lib/App.svelte'

	import screenshot from '$lib/assets/screenshot.png'

	const title = 'SWR Data Lab Boundaries'
	const description = 'Ready-to-use, timestamped boundary data for Germany in the versatiles format.'
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content={description} />

	<meta property="og:url" content="https://www.maxkohler.com/" />
	<meta property="og:type" content="website" />
	<meta property="og:title" content={title} />
	<meta property="og:description" content={description} />
	<meta property="og:image" content={screenshot} />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={title} />
	<meta name="twitter:description" content={description} />
	<meta name="twitter:image" content={screenshot} />
</svelte:head>

<DesignTokens theme="light">
	<App />
</DesignTokens>
