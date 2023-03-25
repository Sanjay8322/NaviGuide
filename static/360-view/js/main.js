import locations from "./viewer_details.js";
import get_current_view_place from './utilities.js';


let viewer_details = {
    type: 'equirectangular',
    autoLoad: true,
    keyboardZoom: true,
    mouseZoom: true,
    showZoomCtrl: true,
    draggable: true,
    friction: 0.01,
    autoRotate: -2
}

var current_view_place = get_current_view_place(window);

if (current_view_place === null ){
    // admin_out is the home location for the college
    viewer_details.panorama = locations.admin_out.panorama;
    viewer_details.hotSpots = locations.admin_out.hotSpots;
}

else{
    viewer_details.panorama = locations[current_view_place].panorama;
    viewer_details.hotSpots = locations[current_view_place].hotSpots;
}

console.log(viewer_details);

var viewer = pannellum.viewer('panorama', viewer_details);

// Do other tasks with the viewer object
