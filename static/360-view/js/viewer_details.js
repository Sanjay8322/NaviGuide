var locations = {
    admin_out: {
        panorama: admin_out,
        hotSpots: [
            {
                pitch: 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Admin Block Interior",
                clickHandlerFunc: function() {
                    // Append query parameter to URL
                    window.location.search += '&current_view_place=' + 'admin_in'
                }
            }
        ]
    },

    admin_in: {
        panorama: admin_in,
        hotSpots: [
            {
                "pitch": 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Baltimore Museum of Art",
                "URL": "https://artbma.org/"
            }
        ]
    },

    library_out: {
        panorama: library_out,
        hotSpots: [
            {
                "pitch": 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Baltimore Museum of Art",
                "URL": "https://artbma.org/"
            }
        ]
    },

    library_in: {
        panorama: library_in,
        hotSpots: [
            {
                "pitch": 14.1,
                "yaw": 1.5,
                "type": "info",
                "text": "Baltimore Museum of Art",
                "URL": "https://artbma.org/"
            }
        ]
    }
}

export default locations;




