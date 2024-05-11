import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { OBJLoader } from     'three/addons/loaders/OBJLoader.js';
import { GUI } from           'three/addons/libs/lil-gui.module.min.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

let num_objects_curr = 0;
let num_objects = 100;


const layers = {
	'Toggle Name': function () {
		console.log('toggle')
		camera.layers.toggle(0);
	}
}

function onDoubleClick(event) {
	mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
	mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
	raycaster.setFromCamera( mouse, camera );
	let intersections = raycaster.intersectObjects( [ threejs_objects['scene0451_01'] ] );
	intersection = ( intersections.length ) > 0 ? intersections[ 0 ] : null;
	console.log(intersections);
}

function get_lines(properties){
    var geometry = new THREE.BufferGeometry();
    let binary_filename = properties['binary_filename'];
    var positions = [];
    let num_lines = properties['num_lines'];

    fetch(binary_filename)
    .then(response => response.arrayBuffer())
    .then(buffer => {
        positions = new Float32Array(buffer, 0, 3 * num_lines * 2);
        let colors_uint8 = new Uint8Array(buffer, (3 * num_lines * 2) * 4, 3 * num_lines * 2);
        let colors_float32 = Float32Array.from(colors_uint8);
        for (let i=0; i<colors_float32.length; i++) {
         	colors_float32[i] /= 255.0;
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors_float32, 3));
    }).then(step_progress_bar).then(render);
	var material = new THREE.LineBasicMaterial({color: 0xFFFFFF, vertexColors: true});
	return new THREE.LineSegments( geometry, material );
}

function get_cube(){
	let cube_geometry = new THREE.BoxGeometry(1, 5, 1);
	let cube_material = new THREE.MeshPhongMaterial({color: 0x00ffff});
	cube_material.wireframe = false;
	cube_material.wireframeLinewidth = 5;
	let cube = new THREE.Mesh(cube_geometry, cube_material);
	return cube
}

function add_progress_bar(){
    let gProgressElement = document.createElement("div");
    const html_code = '<div class="progress">\n' +
		'<div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%" id="progress_bar"></div>\n' +
		'</div>';
    gProgressElement.innerHTML = html_code;
    gProgressElement.id = "progress_bar_id"
    gProgressElement.style.left = "20%";
    gProgressElement.style.right = "20%";
    gProgressElement.style.position = "fixed";
    gProgressElement.style.top = "50%";
    document.body.appendChild(gProgressElement);
}

function step_progress_bar(){
	num_objects_curr += 1.0
	let progress_int = parseInt(num_objects_curr / num_objects * 100.0)
	let width_string = String(progress_int)+'%';
	document.getElementById('progress_bar').style.width = width_string;
	document.getElementById('progress_bar').innerText = width_string;

	if (progress_int==100) {
		document.getElementById( 'progress_bar_id' ).innerHTML = "";
	}
}

function add_watermark(){
	let watermark = document.createElement("div");
    const html_code = '<a href="https://francisengelmann.github.io/pyviz3d/" target="_blank"><b>PyViz3D</b></a>';
    watermark.innerHTML = html_code;
    watermark.id = "watermark"
    watermark.style.right = "5px";
    watermark.style.position = "fixed";
    watermark.style.bottom = "5px";
    watermark.style.color = "#999";
    watermark.style.fontSize = "7ox";
    document.body.appendChild(watermark);
}

function set_camera_properties(properties){
	camera.setFocalLength(properties['focal_length']);
	console.log(camera.getFocalLength);
	camera.up.set(properties['up'][0],
		          properties['up'][1],
				  properties['up'][2]);
	camera.position.set(properties['position'][0],
						properties['position'][1],
						properties['position'][2]);
	update_controls();
	controls.update();
	controls.target = new THREE.Vector3(properties['look_at'][0],
	 	                                properties['look_at'][1],
	 						    		properties['look_at'][2]);
	camera.updateProjectionMatrix();
	controls.update();
}

function get_points(properties){
	// Add points
	// https://github.com/mrdoob/three.js/blob/master/examples/webgl_buffergeometry_points.html
	let positions = [];
	let normals = [];
	let num_points = properties['num_points'];
	let geometry = new THREE.BufferGeometry();
	let binary_filename = properties['binary_filename'];

	fetch(binary_filename)
	    .then(response => response.arrayBuffer())
		.then(buffer => {
			positions = new Float32Array(buffer, 0, 3 * num_points);
			normals = new Float32Array(buffer, (3 * num_points) * 4, 3 * num_points);
		    let colors_uint8 = new Uint8Array(buffer, (3 * num_points) * 8, 3 * num_points);
		    let colors_float32 = Float32Array.from(colors_uint8);
		    for(let i=0; i<colors_float32.length; i++) {
			    colors_float32[i] /= 255.0;
			}
		    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
			geometry.setAttribute('normal', new THREE.Float32BufferAttribute(normals, 3));
			geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors_float32, 3));
		})
		.then(step_progress_bar)
        .then(render);

	 let uniforms = {
        pointSize: { value: properties['point_size'] },
		alpha: {value: properties['alpha']},
		shading_type: {value: properties['shading_type']},
     };

	 let material = new THREE.ShaderMaterial( {
		uniforms:       uniforms,
        vertexShader:   document.getElementById( 'vertexshader' ).textContent,
        fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
        transparent:    true});

	let points = new THREE.Points(geometry, material);
	return points
}

// function get_timepoints(properties,name) {
// 	let binary_filename = properties['binary_filename'];
// 	let shape = properties['shape'];

// 	let new_positions = [];
// 	let new_normals = [];
// 	let colors_float32 = [];
// 	let colors = [];
  
// 	fetch(binary_filename)
// 	  .then(response => response.arrayBuffer())
// 	  .then(buffer => {
// 		let positions = new Float32Array(buffer, 0, shape[0] * shape[1] * 3);

// 		let normals = new Float32Array(buffer, (shape[0] * shape[1] * 3) * 4, shape[0] * shape[1] * 3);

// 		let colors_uint8 = new Uint8Array(buffer, (shape[0] * shape[1] * 3) * 8, shape[0] * shape[1] * 3);
// 		colors_float32 = new Float32Array(colors_uint8);
// 		for (let i = 0; i < colors_float32.length; i++) {
// 		  colors_float32[i] /= 255.0;
// 		}
		
		
// 		for (let i = 0; i < shape[0]; i++) {
// 		  new_positions.push([]);
// 		  new_normals.push([]);
// 		  colors.push([]);
// 		  for (let j = 0; j < shape[1]; j++) {
// 			let positionRow = [];
// 			let normalRow = [];
// 			let colorRow = [];
// 			for (let k = 0; k < shape[2]; k++) {
// 			  let index = (i * shape[1] * shape[2]) + (j * shape[2]) + k;
// 			  positionRow.push(positions[index]);
// 			  normalRow.push(normals[index]);
// 			  colorRow.push(colors_float32[index]);
// 			}
// 			new_positions[i].push(positionRow);
// 			new_normals[i].push(normalRow);
// 			colors[i].push(colorRow);
// 		  }
// 		}
  
// 	  }).then(step_progress_bar)
// 	  .then(render);;
// 	hand_points = new_positions;
// 	hand_normals = new_normals;	
// 	hand_colors = colors;
	
// 	hand_position_index = 0;
	
// 	let nested_dict = {"position": hand_points, 
// 	  					"normal": hand_normals,
// 						"color": hand_colors,
// 						"index": hand_position_index}

// 	time_data[name] = nested_dict
// 	let point = updateHandPosition();
// 	console.log("point:",point);
// 	return point
//   }
function get_timepoints(properties, name) {
    let binary_filename = properties['binary_filename'];
    let shape = properties['shape'];

    let new_positions = [];
    let new_normals = [];
    let colors_float32 = [];
    let colors = [];

    return fetch(binary_filename)
        .then(response => response.arrayBuffer())
        .then(buffer => {
            let positions = new Float32Array(buffer, 0, shape[0] * shape[1] * 3);
            let normals = new Float32Array(buffer, (shape[0] * shape[1] * 3) * 4, shape[0] * shape[1] * 3);
            let colors_uint8 = new Uint8Array(buffer, (shape[0] * shape[1] * 3) * 8, shape[0] * shape[1] * 3);

            colors_float32 = new Float32Array(colors_uint8);
            for (let i = 0; i < colors_float32.length; i++) {
                colors_float32[i] /= 255.0;
            }

            for (let i = 0; i < shape[0]; i++) {
                new_positions.push([]);
                new_normals.push([]);
                colors.push([]);
                for (let j = 0; j < shape[1]; j++) {
                    let positionRow = [];
                    let normalRow = [];
                    let colorRow = [];
                    for (let k = 0; k < shape[2]; k++) {
                        let index = (i * shape[1] * shape[2]) + (j * shape[2]) + k;
                        positionRow.push(positions[index]);
                        normalRow.push(normals[index]);
                        colorRow.push(colors_float32[index]);
                    }
                    new_positions[i].push(positionRow);
                    new_normals[i].push(normalRow);
                    colors[i].push(colorRow);
                }
            }
        }).then(step_progress_bar).then(render)
        .then(() => {

			let start = 0
            let nested_dict = {
                "position": new_positions,
                "normal": new_normals,
                "color": colors,
                "index": start
            };

            time_data[name] = nested_dict;



			const newPositions = new_positions[0];
			const newColor = colors[0];
			const newNormal = new_normals[0];
			
	
			// Create a simple buffer geometry and material for debugging
			const geometry = new THREE.BufferGeometry();
			// const material = new THREE.PointsMaterial({ color: 0xff0000, size: 0.01 }); // Red color
			const flatNormals = newNormal.flat();
			geometry.setAttribute('normal', new THREE.Float32BufferAttribute(flatNormals, 3));
			const ColorNormals = newColor.flat();
			geometry.setAttribute('color', new THREE.Float32BufferAttribute(ColorNormals, 3));
			// Convert the new positions to a flat array for the geometry
			const flatPositions = newPositions.flat();
			geometry.setAttribute('position', new THREE.Float32BufferAttribute(flatPositions, 3));
			
			// Create a new Points object for debugging
			let uniforms = {
				pointSize: { value: 0.1 },
				alpha: {value: 1.0},
				shading_type: {value: 1},
			};

			let material = new THREE.ShaderMaterial( {
				uniforms:       uniforms,
				vertexShader:   document.getElementById( 'vertexshader' ).textContent,
				fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
				transparent:    true});

			let hand_points_object = new THREE.Points(geometry, material);
			
			return hand_points_object;


        })
        .then(point => {
            return point;
        })
        .catch(error => {
            console.error('Error fetching or processing data:', error);
        });
}

function get_labels(properties){
	const labels = new THREE.Group();
	labels.name = "labels"
	for (let i=0; i<properties['labels'].length; i++){
		const labelDiv = document.createElement('div');
		labelDiv.className = 'label';
		labelDiv.style.color = "rgb("+properties['colors'][i][0]+", "+properties['colors'][i][1]+", "+properties['colors'][i][2]+")"; 
		labelDiv.textContent = properties['labels'][i];
	
		const label_2d = new CSS2DObject(labelDiv);
		label_2d.position.set(properties['positions'][i][0], properties['positions'][i][1], properties['positions'][i][2]);
		labels.add(label_2d);
	}
	return labels
}

function get_circles_2d(properties){
	const labels = new THREE.Group();
	labels.name = "labels"
	for (let i=0; i<properties['labels'].length; i++){
		const border_color = "rgb("+properties['border_colors'][i][0]+", "+properties['border_colors'][i][1]+", "+properties['border_colors'][i][2]+")";
		const fill_color = "rgb("+properties['fill_colors'][i][0]+", "+properties['fill_colors'][i][1]+", "+properties['fill_colors'][i][2]+")";
		const labelDiv = document.createElement('div');
		labelDiv.className = 'label';
		labelDiv.textContent = properties['labels'][i];
		labelDiv.style.border = '3px solid '+border_color;
		labelDiv.style.backgroundColor = fill_color;
		labelDiv.style.borderRadius = '30px';
		const label_2d = new CSS2DObject(labelDiv);
		label_2d.position.set(properties['positions'][i][0], properties['positions'][i][1], properties['positions'][i][2]);
		labels.add(label_2d);
	}
	return labels
}

function get_obj(properties){
	var container = new THREE.Object3D();
	function loadModel(object) {
		object.traverse(
		function(child) {
			if (child.isMesh) {
				let r = properties['color'][0]
				let g = properties['color'][1]
				let b = properties['color'][2]
				let colorString = "rgb("+r+","+g+", "+b+")"
				child.material.color.set(new THREE.Color(colorString));
			}
		});
		object.translateX(properties['translation'][0])
		object.translateY(properties['translation'][1])
		object.translateZ(properties['translation'][2])

		const q = new THREE.Quaternion(
			properties['rotation'][1],
			properties['rotation'][2],
			properties['rotation'][3],
			properties['rotation'][0])
		object.setRotationFromQuaternion(q)

		object.scale.set(properties['scale'][0], properties['scale'][1], properties['scale'][2])

		container.add(object)
		step_progress_bar();
		render();
	}

	const loader = new OBJLoader();
	loader.load(properties['filename'], loadModel,
				function (xhr){ // called when loading is in progresses
					console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
				},
				function (error){ // called when loading has errors
					console.log( 'An error happened' );
				});
	return container
}

function get_material(alpha){
	let uniforms = {
		alpha: {value: alpha},
		shading_type: {value: 1},
	};
	let material = new THREE.ShaderMaterial({
		uniforms:       uniforms,
		vertexShader:   document.getElementById('vertexshader').textContent,
		fragmentShader: document.getElementById('fragmentshader').textContent,
		transparent:    true,
    });
    return material;
}

function set_geometry_vertex_color(geometry, color){
	const r = Math.fround(color[0] / 255.0);
	const g = Math.fround(color[1] / 255.0);
	const b = Math.fround(color[2] / 255.0);
	const num_vertices = geometry.getAttribute('position').count;
	const colors = new Float32Array(num_vertices * 3);
	for (let i = 0; i < num_vertices; i++){
		colors[3 * i + 0] = r;
		colors[3 * i + 1] = g;
		colors[3 * i + 2] = b;
	}
	geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
}

function get_cylinder_geometry(radius_top, radius_bottom, height, radial_segments, color){
	let geometry = new THREE.CylinderGeometry(radius_top, radius_bottom, height, radial_segments);
	set_geometry_vertex_color(geometry, color)
	return geometry;
}

function get_sphere_geometry(radius, widthSegments, heightSegments, color){
	const geometry = new THREE.SphereGeometry(radius, widthSegments, heightSegments);
	set_geometry_vertex_color(geometry, color);
	return geometry;
}

function get_cuboid(properties){
	const radius_top = properties['edge_width'];
	const radius_bottom = properties['edge_width'];
	const radial_segments = 30;
	const height = 1;
	
	let geometry = get_cylinder_geometry(
		radius_top, radius_bottom, height, radial_segments,
		properties['color']);
	let material = get_material(properties['alpha']);

	const cylinder_x = new THREE.Mesh(geometry, material);
	cylinder_x.scale.set(1.0, properties['size'][0], 1.0)
	cylinder_x.rotateZ(3.1415/2.0)
	const cylinder_00 = cylinder_x.clone()
	cylinder_00.position.set(0, -properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const cylinder_01 = cylinder_x.clone()
	cylinder_01.position.set(0, properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const cylinder_20 = cylinder_x.clone()
	cylinder_20.position.set(0, -properties['size'][1]/2.0, properties['size'][2]/2.0)
	const cylinder_21 = cylinder_x.clone()
	cylinder_21.position.set(0, properties['size'][1]/2.0, properties['size'][2]/2.0)

	const cylinder_y = new THREE.Mesh(geometry, material);
	cylinder_y.scale.set(1.0, properties['size'][1], 1.0)
	const cylinder_02 = cylinder_y.clone()
	cylinder_02.position.set(-properties['size'][0]/2.0, 0, -properties['size'][2]/2.0)
	const cylinder_03 = cylinder_y.clone()
	cylinder_03.position.set(properties['size'][0]/2.0, 0, -properties['size'][2]/2.0)
	const cylinder_22 = cylinder_y.clone()
	cylinder_22.position.set(-properties['size'][0]/2.0, 0, properties['size'][2]/2.0)
	const cylinder_23 = cylinder_y.clone()
	cylinder_23.position.set(properties['size'][0]/2.0, 0, properties['size'][2]/2.0)

	const cylinder_z = new THREE.Mesh(geometry, material);
	cylinder_z.scale.set(1.0, properties['size'][2], 1.0)
	cylinder_z.rotateX(3.1415/2.0)
	const cylinder_10 = cylinder_z.clone()
	cylinder_10.position.set(-properties['size'][0]/2.0, -properties['size'][1]/2.0, 0.0)
	const cylinder_11 = cylinder_z.clone()
	cylinder_11.position.set(properties['size'][0]/2.0, -properties['size'][1]/2.0, 0.0)
	const cylinder_12 = cylinder_z.clone()
	cylinder_12.position.set(-properties['size'][0]/2.0, properties['size'][1]/2.0, 0.0)
	const cylinder_13 = cylinder_z.clone()
	cylinder_13.position.set(properties['size'][0]/2.0, properties['size'][1]/2.0, 0.0)

	let corner_geometry = get_sphere_geometry(properties['edge_width'], 30, 30, properties['color']);

	const sphere = new THREE.Mesh(corner_geometry, material);
	const corner_00 = sphere.clone()
	corner_00.position.set(-properties['size'][0]/2.0, -properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_01 = sphere.clone()
	corner_01.position.set(properties['size'][0]/2.0, -properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_02 = sphere.clone()
	corner_02.position.set(-properties['size'][0]/2.0, properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_03 = sphere.clone()
	corner_03.position.set(properties['size'][0]/2.0, properties['size'][1]/2.0, -properties['size'][2]/2.0)
	const corner_10 = sphere.clone()
	corner_10.position.set(-properties['size'][0]/2.0, -properties['size'][1]/2.0, properties['size'][2]/2.0)
	const corner_11 = sphere.clone()
	corner_11.position.set(properties['size'][0]/2.0, -properties['size'][1]/2.0, properties['size'][2]/2.0)
	const corner_12 = sphere.clone()
	corner_12.position.set(-properties['size'][0]/2.0, properties['size'][1]/2.0, properties['size'][2]/2.0)
	const corner_13 = sphere.clone()
	corner_13.position.set(properties['size'][0]/2.0, properties['size'][1]/2.0, properties['size'][2]/2.0)

	const cuboid = new THREE.Group();
	cuboid.position.set(properties['position'][0], properties['position'][1], properties['position'][2])
	cuboid.add(cylinder_00)
	cuboid.add(cylinder_01)
	cuboid.add(cylinder_20)
	cuboid.add(cylinder_21)
	cuboid.add(cylinder_02)
	cuboid.add(cylinder_03)
	cuboid.add(cylinder_22)
	cuboid.add(cylinder_23)
	cuboid.add(cylinder_10)
	cuboid.add(cylinder_11)
	cuboid.add(cylinder_12)
	cuboid.add(cylinder_13)

	cuboid.add(corner_00)
	cuboid.add(corner_01)
	cuboid.add(corner_02)
	cuboid.add(corner_03)
	cuboid.add(corner_10)
	cuboid.add(corner_11)
	cuboid.add(corner_12)
	cuboid.add(corner_13)

	const q = new THREE.Quaternion(
			properties['orientation'][1],
			properties['orientation'][2],
			properties['orientation'][3],
			properties['orientation'][0])
	cuboid.setRotationFromQuaternion(q)
	cuboid.position.set(properties['position'][0], properties['position'][1], properties['position'][2])
	return cuboid
}

function get_polyline(properties){
	const radius_top = properties['edge_width']
	const radius_bottom = properties['edge_width']
	const radial_segments = 5;
	const height = 1;
	let material = get_material(properties['alpha']);
	let geometry = get_cylinder_geometry(radius_top, radius_bottom, height, radial_segments, properties['color']);
	const cylinder = new THREE.Mesh(geometry, material);
	let corner_geometry = get_sphere_geometry(properties['edge_width'], radial_segments, radial_segments, properties['color']);
	const sphere = new THREE.Mesh(corner_geometry, material);
	const polyline = new THREE.Group();

	// Add first corner to the polyline
	const corner_0 = sphere.clone()
	corner_0.position.set(properties['positions'][0][0], properties['positions'][0][1], properties['positions'][0][2])
	polyline.add(corner_0)

	for (var i=1; i < properties['positions'].length; i++){
		// Put the sphere the make a nice round corner
		const corner_i = sphere.clone()
		corner_i.position.set(properties['positions'][i][0],
			                  properties['positions'][i][1],
			                  properties['positions'][i][2])

		// Put a segment connecting the two last points
		const cylinder_i = cylinder.clone()
		var dist_x = properties['positions'][i][0] - properties['positions'][i-1][0]
		var dist_y = properties['positions'][i][1] - properties['positions'][i-1][1]
		var dist_z = properties['positions'][i][2] - properties['positions'][i-1][2]
		var cylinder_length = Math.sqrt(dist_x*dist_x + dist_y*dist_y + dist_z*dist_z)
		cylinder_i.scale.set(1.0, cylinder_length, 1.0)
		cylinder_i.lookAt(properties['positions'][i][0] - properties['positions'][i-1][0],
	                      properties['positions'][i][1] - properties['positions'][i-1][1],
	                      properties['positions'][i][2] - properties['positions'][i-1][2])
		cylinder_i.rotateX(3.1415/2.0)
		cylinder_i.position.set(properties['positions'][i-1][0],
			                    properties['positions'][i-1][1],
		                        properties['positions'][i-1][2])
		cylinder_i.translateY(cylinder_length/2.0)
		polyline.add(cylinder_i)
	}

	return polyline
}

function get_arrow(properties){
	const radius_top = 0.0;
	const radius_bottom = properties['head_width'];
	const radial_segments = 15;
	const height = radius_bottom * 2.0;

	var dist_x = properties['end'][0] - properties['start'][0]
	var dist_y = properties['end'][1] - properties['start'][1]
	var dist_z = properties['end'][2] - properties['start'][2]
	var margnitude = Math.sqrt(dist_x*dist_x + dist_y*dist_y + dist_z*dist_z)

	let material = get_material(properties['alpha']);
	let geometry = get_cylinder_geometry(radius_top, radius_bottom, height, radial_segments, properties['color']);
	let geometry_stroke = get_cylinder_geometry(properties['stroke_width'], properties['stroke_width'], margnitude - height, radial_segments, properties['color']);

	const arrow_head = new THREE.Mesh(geometry, material);
	arrow_head.translateY(margnitude - height / 2.0)
	const arrow_stroke = new THREE.Mesh(geometry_stroke, material);
	arrow_stroke.translateY(margnitude / 2.0 - height / 2.0)

	const arrow = new THREE.Group();
	arrow.add(arrow_head);
	arrow.add(arrow_stroke);

	arrow.lookAt(properties['end'][0] - properties['start'][0],
		              properties['end'][1] - properties['start'][1],
		              properties['end'][2] - properties['start'][2])
	arrow.rotateX(3.1415/2.0)
	arrow.position.set(properties['start'][0], properties['start'][1], properties['start'][2] )
	return arrow;
}

function get_ground(){
	let mesh = new THREE.Mesh(new THREE.PlaneBufferGeometry(2000, 2000),
							  new THREE.MeshPhongMaterial({ color: 0x999999, depthWrite: true}));
	mesh.rotation.x = -Math.PI / 2;
	mesh.position.set(0, -5, 0);
	mesh.receiveShadow = true;
	return mesh;
}



function init_gui(objects){
	let menuMap = new Map();
	for (const [name, value] of Object.entries(objects)){
		let splits = name.split(';');
		if (splits.length > 1) {
			let folder_name = splits[0];
			if (!menuMap.has(folder_name)) {
				menuMap.set(folder_name, gui.addFolder(folder_name));
			}
			let fol = menuMap.get(folder_name);
			fol.add(value, 'visible').name(splits[1]).onChange(render);
			fol.open();
		} else {
			// if (value.name.localeCompare('labels') != 0) {
			// 	gui.add(value, 'visible').name(name).onChange(render);
			// }
			if (value && value.name && value.name.localeCompare('labels') != 0) {
				gui.add(value, 'visible').name(name).onChange(render);
			}
		}
	}
}

let startTime;

function updateTimer() {
    const currentTime = new Date().getTime();
    const elapsedTime = currentTime - startTime;

    const hours = Math.floor(elapsedTime / (1000 * 60 * 60));
    const minutes = Math.floor((elapsedTime % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);
    const milliseconds = Math.floor(elapsedTime % 1000);

    const timerElement = document.getElementById('timer');
    timerElement.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}:${milliseconds.toString().padStart(3, '0')}`;
	
    requestAnimationFrame(updateTimer);
	render();
}

function render() {
    renderer.render(scene, camera);
	labelRenderer.render(scene, camera);
}

function init(){
	scene.background = new THREE.Color(0xffffff);
	renderer.setSize(window.innerWidth, window.innerHeight);
	labelRenderer.setSize(window.innerWidth, window.innerHeight);

	let hemiLight = new THREE.HemisphereLight( 0xffffff, 0x444444 );
	hemiLight.position.set(0, 20, 0);
	//scene.add(hemiLight);

	let dirLight = new THREE.DirectionalLight( 0xffffff );
	dirLight.position.set(-10, 10, - 10);
	dirLight.castShadow = true;
	dirLight.shadow.camera.top = 2;
	dirLight.shadow.camera.bottom = - 2;
	dirLight.shadow.camera.left = - 2;
	dirLight.shadow.camera.right = 2;
	dirLight.shadow.camera.near = 0.1;
	dirLight.shadow.camera.far = 40;
	//scene.add(dirLight);

	let intensity = 0.5;
	let color = 0xffffff;
	const spotLight1 = new THREE.SpotLight(color, intensity);
	spotLight1.position.set(100, 1000, 0);
	scene.add(spotLight1);
	const spotLight2 = new THREE.SpotLight(color, intensity/3.0);
	spotLight2.position.set(100, -1000, 0);
	scene.add(spotLight2);
	const spotLight3 = new THREE.SpotLight(color, intensity);
	spotLight3.position.set(0, 100, 1000);
	scene.add(spotLight3);
	const spotLight4 = new THREE.SpotLight(color, intensity/3.0);
	spotLight4.position.set(0, 100, -1000);
	scene.add(spotLight4);
	const spotLight5 = new THREE.SpotLight(color, intensity);
	spotLight5.position.set(1000, 0, 100);
	scene.add(spotLight5);
	const spotLight6 = new THREE.SpotLight(color, intensity/3.0);
	spotLight6.position.set(-1000, 0, 100);
	scene.add(spotLight6);

	raycaster = new THREE.Raycaster();
	raycaster.params.Points.threshold = 1.0;
	startTime = new Date().getTime();
    updateTimer();
}

async function create_threejs_objects(properties){

	num_objects_curr = 0.0;
	num_objects = parseFloat(Object.entries(properties).length);

	for (const [object_name, object_properties] of Object.entries(properties)) {
		if (String(object_properties['type']).localeCompare('camera') == 0){
			set_camera_properties(object_properties);
			render();
    		step_progress_bar();
    		continue;
		}
		if (String(object_properties['type']).localeCompare('points') == 0){
			threejs_objects[object_name] = get_points(object_properties);
    		render();
		}
		if (String(object_properties['type']).localeCompare('labels') == 0){
			threejs_objects[object_name] = get_labels(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('circles_2d') == 0){
			threejs_objects[object_name] = get_circles_2d(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('lines') == 0){
			threejs_objects[object_name] = get_lines(object_properties);
    		render();
		}
		if (String(object_properties['type']).localeCompare('obj') == 0){
			threejs_objects[object_name] = get_obj(object_properties);
		}
		if (String(object_properties['type']).localeCompare('cuboid') == 0){
			threejs_objects[object_name] = get_cuboid(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('polyline') == 0){
			threejs_objects[object_name] = get_polyline(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('arrow') == 0){
			threejs_objects[object_name] = get_arrow(object_properties);
			step_progress_bar();
			render();
		}
		if (String(object_properties['type']).localeCompare('timepoints') == 0){
			threejs_objects[object_name] = await get_timepoints(object_properties,object_name);
			render();
		}
		
		threejs_objects[object_name].visible = object_properties['visible'];
		threejs_objects[object_name].frustumCulled = false;
	}
	
	// Add axis helper
	threejs_objects['Axis'] = new THREE.AxesHelper(1);

	render();
}

function add_threejs_objects_to_scene(threejs_objects){
	for (const [key, value] of Object.entries(threejs_objects)) {
		scene.add(value);
	}
}

function onWindowResize(){
    const innerWidth = window.innerWidth
    const innerHeight = window.innerHeight;
    renderer.setSize(innerWidth, innerHeight);
    labelRenderer.setSize(innerWidth, innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    render();
}

function update_controls(){
	controls = new OrbitControls(camera, labelRenderer.domElement);
	controls.addEventListener("change", render);
	controls.enableKeys = true;
	controls.enablePan = true; // enable dragging
}

function updateColors() {
    // Update the color properties of the objects based on the current timestep
    for (const [object_name, object] of Object.entries(threejs_objects)) {
        if (object.material) {
            // Check if the object is an arrow
		
            if (object_name.startsWith("Axis")) {
                // Update the color of the arrow material
				object.material.color.setRGB(Math.sin(Date.now() * 0.001), Math.cos(Date.now() * 0.001), Math.tan(Date.now() * 0.001));
                // object.material.uniforms.alpha.value = Math.sin(Date.now() * 0.001); // Example color change based on timestamp
            } 
        }
    }

    // Re-render the scene after updating the object properties
    render();
}
function updatePoints() {
	const timerElement = document.getElementById('timer');
	const timerValue = timerElement.textContent;
	
	for (const [object_name, object] of Object.entries(threejs_objects)) {
		const objectNameParts = object_name.split(' ');
		if (objectNameParts.length > 1) {
			
		const objectTimeParts = objectNameParts[1].split(';');
		const milliObjectTimeParts = objectNameParts[1].split('.');
		if (objectTimeParts.length === 3) {
			
			// const objectTime = `${objectTimeParts[0].padStart(2, '0')}:${objectTimeParts[1].padStart(2, '0')}:${objectTimeParts[2].replace(/\.\d{0}/, ':')}`;
			const objectTime = `${objectTimeParts[0].padStart(2, '0')}:${objectTimeParts[1].padStart(2, '0')}:${objectTimeParts[2].replace(/\..*/, '')}`;


			const timerTimeParts = timerValue.split(':');
			// const timerTime = `${timerTimeParts[0].padStart(2, '0')}:${timerTimeParts[1].padStart(2, '0')}:${timerTimeParts[2].padStart(2, '0')}:${timerTimeParts[3].padStart(2, '0')}`;
			const timerTime = `${timerTimeParts[0].padStart(2, '0')}:${timerTimeParts[1].padStart(2, '0')}:${timerTimeParts[2].padStart(2, '0')}`;

			if (objectTime == timerTime) {
				console.log("visible");
			threejs_objects[object_name].visible = true;
			} else {
			threejs_objects[object_name].visible = false;
			}
		}
		}
	}
  }


const scene = new THREE.Scene();

const renderer = new THREE.WebGLRenderer({antialias: true});
document.getElementById('render_container').appendChild(renderer.domElement)

var camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.01, 1000);
var controls = '';

let labelRenderer = new CSS2DRenderer();
labelRenderer.setSize( window.innerWidth, window.innerHeight );
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0px';
document.getElementById('render_container').appendChild(labelRenderer.domElement)

window.addEventListener('resize', onWindowResize, false);

let raycaster;
let intersection = null;
let mouse = new THREE.Vector2();

const gui = new GUI({autoPlace: true, width: 120});

// dict containing all objects of the scene
let threejs_objects = {};

let time_data = {};

init();

// Load nodes.json and perform one after the other the following commands:
fetch('nodes.json')
	.then(response => {add_progress_bar(); return response;})
    .then(response => {return response.json();})
    // .then(json_response => {console.log(json_response); return json_response})
    .then(json_response => create_threejs_objects(json_response))
    .then(() => add_threejs_objects_to_scene(threejs_objects))
    .then(() => init_gui(threejs_objects))
	.then(() => console.log('Done'))
	.then(() => console.log(threejs_objects))
	.then(() => {
        setInterval(updateHandPosition, 100);
        setInterval(updateTimer, 10);
		render();
    });

function updateHandPosition() {

	for (let key in time_data) 
	{
		if (time_data.hasOwnProperty(key)) 
		{
			let nestedDict = time_data[key];
			nestedDict["index"] = nestedDict["index"] + 1; 
			if (nestedDict["index"] >= nestedDict.position.length) {
				nestedDict["index"] = 0;
			}
			
			

			const newPositions = nestedDict.position[nestedDict["index"]];
			const newColor = nestedDict.color[nestedDict["index"]];
			const newNormal = nestedDict.normal[nestedDict["index"]];
			
	
			// Get the existing geometry and material from the threejs_objects object
			const geometry = threejs_objects[key].geometry;
			const material = threejs_objects[key].material;
			material.uniforms.pointSize.value = 10; // Set the new point size
            material.uniforms.alpha.value = 1.0; // Set the new alpha value
            material.uniforms.shading_type.value = 1;
			// const material = new THREE.PointsMaterial({ color: 0xff0000, size: 0.01 }); // Red color
			const flatNormals = newNormal.flat();
			geometry.setAttribute('normal', new THREE.Float32BufferAttribute(flatNormals, 3));
			const flatColors = newColor.flat();
			geometry.setAttribute('color', new THREE.Float32BufferAttribute(flatColors, 3));
			// Convert the new positions to a flat array for the geometry
			const flatPositions = newPositions.flat();
			geometry.setAttribute('position', new THREE.Float32BufferAttribute(flatPositions, 3));

			// If you need to recompile the shader
			material.needsUpdate = true;
			
			geometry.attributes.position.needsUpdate = true;
			geometry.attributes.normal.needsUpdate = true;
			geometry.attributes.color.needsUpdate = true;

		}
	}
}
document.getElementById('reset_button').onclick = function() {
    // Handle button click here
	resetTime();
};
// document.getElementById("reset_button").onclick = () => myFunction();
function resetTime() {
	for (let key in time_data) 
	{
		if (time_data.hasOwnProperty(key)) 
		{	
			let nestedDict = time_data[key];
			nestedDict["index"] = 0; 
		}
	}
	// Reset the start time to the current time
	startTime = new Date().getTime();
};
