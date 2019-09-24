$(document).ready(function() {
    var table = $("#frametable").DataTable({
        paging: false,
        searching: false,
        fixedHeader: true,
        ajax: 'data/frames/steve.json',
        columns: [
            { title: 'Input' },
            { title: 'Startup' },
            { title: 'Block' },
            { title: 'Hit' },
            { title: 'Counter' },
            { title: 'Level' },
            { title: 'Damage' }
    ]
    });

    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    // Event listener to the two range filtering inputs to redraw on input
    $("#allCheckbox").change(function() {
        if ($(this).is(":checked")) {
            $('input[type=checkbox]').each(function(index) {
                $(this)[0].checked = true;
            });

            $.fn.dataTable.ext.search.pop();
        } else {
            $('input[type=checkbox]').each(function(index) {
                $(this)[0].checked = false;
            });
            $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
                return false;
            });
        }
        table.draw();
    });


    $('#dismiss, .overlay').on('click', function() {
        // hide sidebar
        $('#sidebar').removeClass('active');
        // hide overlay
        $('.overlay').removeClass('active');
    });

    $('#sidebarCollapse').on('click', function() {
        // open sidebar
        $('#sidebar').addClass('active');
        // fade in the overlay
        $('.overlay').addClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
});

function bodyClicked() {
    if (typeof buttonNav.opened == 'undefined') {
        return;
    }
    if (buttonNav.opened) {
        closeNav();
    }
}


function openNav() {
    console.log("opening");
    document.getElementById("mySidebar").style.width = "200px";
    document.getElementById("main").style.marginLeft = "200px";
    buttonNav.opened = true;
}

function closeNav() {
    console.log("closing");
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    buttonNav.opened = false;
}


function buttonNav() {
    if (typeof buttonNav.opened == 'undefined') {
        buttonNav.opened = true;
    }
    if (buttonNav.opened) {
        closeNav();
    } else {
        openNav();
    }
}