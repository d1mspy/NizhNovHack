<script lang="ts">
	import favicon from '/cute_minion.png';
	import "../global.css";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children?.()}

<style>
	:global(html, body) {
		height: auto !important;
		overflow-y: auto !important;
	}
</style>