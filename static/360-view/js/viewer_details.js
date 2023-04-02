
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
            },
            {
                "name": "Way to Kore",
                "pitch": -3.392,
                "yaw": 64.06,
                "type": "info",
                "text": "Way to Kore"
            },
            {
                "name": "Way to CCD",
                "pitch": -1.424,
                "yaw": -60.980,
                "type": "info",
                "text": "Way to CCD"
            },
            
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
            },
            {
                "name": "Cash Counter / Admission office",
                "pitch": -4.30574,
                "yaw": 119.694,
                "type": "info",
                "text": "Cash Counter / Admission office"
            },
            {
                "name": "KCLAS",
                "pitch": -4.4565,
                "yaw": -129.07,
                "type": "info",
                "text": "KCLAS"
            },
            {
                "name": "Way to auditorium",
                "pitch": -2.5564,
                "yaw": -17.782,
                "type": "info",
                "text": "Way to auditorium"
            },
            {
                "name": "Restroom",
                "pitch": -2.03648,
                "yaw": 13.926,
                "type": "info",
                "text": "Restroom"
            },
            

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
            },
        ]
    }
}

export default locations;




