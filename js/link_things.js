function process_thing(thing) {
	thing.style["fill-opacity"] = .5;
	thing.onmouseover = function() {
		this.style.cursor = "pointer";
	};
	thing.onclick = function() {
		window.open(`build/things/${thing.id}.html`, '_blank').focus();
	};
}

document.addEventListener("DOMContentLoaded", (event) => {
	console.log("Hi!");

	const things_layer = document.getElementById("things");

	for (let thing  of things_layer.children) {
		process_thing(thing);
	}

	console.log(things_layer.children);
});


