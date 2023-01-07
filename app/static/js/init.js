/*!
 * graphs.wwdt.me (https://github.com/questionlp/graphs.wwdt.me_v2)
 * Copyright 2018-2023 Linh Pham
 * Apache License 2.0 (https://github.com/questionlp/graphs.wwdt.me_v2/blob/main/LICENSE)
 */

document.addEventListener('DOMContentLoaded', function () {
    var sidenav_elems = document.querySelectorAll(".sidenav");
    var dropdown_elems = document.querySelectorAll(".dropdown-trigger");
    var collapsible_elems = document.querySelectorAll(".collapsible");

    var dropdown_options = {
        "alignment": "right",
        "autoTrigger": true,
        "constrainWidth": false,
        "coverTrigger": false,
        "hover": false,
        "inDuration": 100,
        "outDuration": 125
    };

    var sidenav_instances = M.Sidenav.init(sidenav_elems);
    var dropdown_instances = M.Dropdown.init(dropdown_elems, dropdown_options);
    var collapsible_instances = M.Collapsible.init(collapsible_elems);
});
