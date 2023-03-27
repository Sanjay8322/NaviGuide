
let getUrlQueryAppendingFunction = (location_name) => {
    let returnableFunction = () => {
        var searchParams = new URLSearchParams(window.location.search);
        searchParams.set('current_view_place', location_name);
        var newParams = searchParams.toString();
        window.location.search = newParams;
    }
    return returnableFunction;
}

var locations = {
    admin_out: {
        panorama: admin_out,
        hotSpots: [
            {
                "name": "Admin In Hotspot",
                "pitch": 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Admin Block Interior",
                clickHandlerFunc: getUrlQueryAppendingFunction('admin_in')
            },

            {
                "name": "Photo taken location",
                "pitch": -82.85,
                "yaw": 173.88,
                "type": "info",
                "text": "Photo was clicked from here"
            }
        ]
    },

    admin_in: {
        panorama: admin_in,
        hotSpots: [
            {
                "name": "Library Hotspot",
                "pitch": 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Mahatma Gandhi Library",
                clickHandlerFunc: getUrlQueryAppendingFunction('library_out')
            }
        ]
    },

    library_out: {
        panorama: library_out,
        hotSpots: [
            {
                "name": "Library In Hotspot",
                "pitch": 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Library In - Books",
                clickHandlerFunc: getUrlQueryAppendingFunction('library_in')
            }
        ]
    },

    library_in: {
        panorama: library_in,
        hotSpots: [
            {
                "name": "Library Out Hotspot",
                "pitch": 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Mahatma Gandhi Library",
                clickHandlerFunc: getUrlQueryAppendingFunction('library_out')
            }
        ]
    }
}

export default locations;




