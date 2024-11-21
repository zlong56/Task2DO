if(document.getElementById("multiselect-basic")){
var multiSelectBasic = document.getElementById("multiselect-basic"),
    multiSelectHeader = (multiSelectBasic && multi(multiSelectBasic, {
        enable_search: !1
    }), document.getElementById("multiselect-header")),
    multiSelectOptGroup = (multiSelectHeader && multi(multiSelectHeader, {
        non_selected_header: "Cars",
        selected_header: "Favorite Cars"
    }), document.getElementById("multiselect-optiongroup"))
}
