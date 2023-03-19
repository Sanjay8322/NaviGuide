// Create the viewer object
console.log(image_url)

viewer_details = {
    type: 'equirectangular',
    panorama: image_url,
    autoLoad: true,
    keyboardZoom: true,
    mouseZoom: true,
    showZoomCtrl: true,
    draggable: true,
    friction: 0.01
}

var viewer = pannellum.viewer('panorama', viewer_details);
// Do other tasks with the viewer object
