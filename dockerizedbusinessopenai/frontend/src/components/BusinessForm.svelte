<script lang="ts">
	import { writable } from 'svelte/store';
	import { setContext } from 'svelte';
	import { aiResponse } from '../store/store';
	let name: string;
	let idea: string;
	let competitors: string;
	let loading: boolean = false;
	let response: string;

	const handleSubmit: any = (e: Event) => {
		e.preventDefault();
		loading = true;

		// Make an HTTP request to the backend
		fetch('http://localhost:9999/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				business_name: name,
				business_idea: idea,
				domains: competitors
			})
		})
			.then((response) => response.json())
			.then((data) => {
				loading = false;
				aiResponse.set(data['choices'][0]['message']['content']);
				})
			.catch((error) => {
				console.log(error);
				loading = false;
				response = error;
			});
	};
</script>

<form on:submit={handleSubmit}>
	<div class="flex flex-col mt-12 mr-20">
		<label for="inputField" class="text-sm font-medium text-gray-700">Your business name</label>
		<input id="inputField" type="text" class="px-3 py-2 mt-1 border rounded-md" bind:value={name} />
	</div>

	<div class="flex flex-col mt-12 mr-20">
		<label for="inputField" class="text-sm font-medium text-gray-700"
			>Tell us what your business idea is!</label
		>
		<input id="inputField" type="text" class="px-3 py-2 mt-1 border rounded-md" bind:value={idea} />
	</div>
	<div class="flex flex-col mt-12 mr-20">
		<label for="inputField" class="text-sm font-medium text-gray-700"
			>List your competitors websites by their website. (comma seperated)</label
		>
		<textarea class="px-3 py-2 mt-1 border rounded-md h-64" bind:value={competitors} />
	</div>

	<div>
		{#if !loading}
			<button type="submit" class="p-6 text-xl bg-stone-600 rounded mt-10 text-white">
				SUBMIT
			</button>
		{:else}
			<div class="p-6 text-xl bg-stone-600 rounded mt-10 text-white">LOADING</div>
		{/if}

		{#if response}
			<div class="p-6 text-xl bg-stone-600 rounded mt-10 text-black">{response}</div>
		{/if}
	</div>
</form>
