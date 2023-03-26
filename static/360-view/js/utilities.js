// Get current URL

let get_current_view_place = (window) => {
    var params = window.location.search
    params = new URLSearchParams(params)
    var current_view = params.get('current_view_place')
    console.log(current_view)

    return current_view;
}

export default get_current_view_place;
