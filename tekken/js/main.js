const CHARACTERS = ["Akuma",
"Alisa Bosconovitch",
"Anna Williams",
"Armor King",
"Asuka Kazama",
"Bob Richards",
"Bryan Fury",
"Claudio Serafino",
"Craig Marduk",
"Devil Jin",
"Eddy Gordo",
"Eliza",
"Feng Wei",
"Geese Howard",
"Gigas",
"Heihachi Mishima",
"Hwoarang",
"Jack-7",
"Jin Kazama",
"Josie Rizal",
"Julia Chang",
"Katarina Alves",
"Kazumi Mishima",
"Kazuya Mishima",
"King",
"Kuma",
"Lars Alexandersson",
"Lee Chaolan",
"Lei Wulong",
"Leo Kliesen",
"Leroy Smith",
"Lili De Rochefort",
"Ling Xiaoyu",
"Lucky Chloe",
"Marshall Law",
"Master Raven",
"Miguel Caballero Rojo",
"Negan",
"Nina Williams",
"Noctis Lucis Caelum",
"Panda",
"Paul Phoenix",
"Sergei Dragunov",
"Shaheen",
"Steve Fox",
"Yoshimitsu",
"Zafina"
]

class APP {
    static FrameTable = null;
    static CurrentPage = "Steve Fox";
    static CurrentCharacter = "Steve Fox";

    static InitializeSideBar() {
        $("#sidebar").mCustomScrollbar({
            theme: "minimal"
        });

        $('#sidebarButton').on('click', toggleSidebar);

        CHARACTERS.forEach((o) => {
            let chars = $('#characters-list');
            chars.append(`<li><a href=\"#\">${o}</a></li>`);
        });

        $("#characters-list").on("click", (e) => {
            toggleSidebar(e);
            charSelect(e, e.target.text);
        });

        $('#dismiss, .overlay').on('click', toggleSidebar);
    }

    static InitializeDataTable() {
        APP.FrameTable = $("#frametable").DataTable({
            paging: false,
            searching: false,
            fixedHeader: true,
            ajax: 'data/frames/Steve Fox.json',
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
    }

    static InitializeFooTable() {
        $('#frametable').footable({
            columns: [
                { title: 'Input' },
                { title: 'Startup' },
                { title: 'Block' },
                { title: 'Hit' },
                { title: 'Counter' },
                { title: 'Level' },
                { title: 'Damage' }
      ],
            "rows": []
        });
    }
};

function toggleSidebar(e) {
    if (typeof toggleSidebar.active != 'undefined') {
        if (toggleSidebar.active) {
            console.log("hiding sidebar");
            // Sidebar is already active: hide it
            $('#sidebar').removeClass('active'); // hide sidebar
            $('.overlay').removeClass('active'); // hide overlay
        } else {
            // Sidebar is toggled: activate it
            console.log("activating sidebar");
            $('#sidebar').addClass('active'); // open sidebar
            // fade in the overlay
            $('.overlay').addClass('active');
            $('.collapse.in').toggleClass('in');
            $('a[aria-expanded=true]').attr('aria-expanded', 'false');
        }
        toggleSidebar.active = !toggleSidebar.active;
        console.log("Sidebar:" + toggleSidebar.active);
        return;
    }
    toggleSidebar.active = false;
}

function loadCharacter(name) {
    APP.CurrentCharacter = name;
    APP.FrameTable = $("#frametable").dataTable({
        "destroy": true,
        paging: false,
        searching: false,
        fixedHeader: true,
        ajax: 'data/frames/' + name + ".json",
    });
}

function charSelect(e, name) {
    loadCharacter(name);
    console.log(name);

}

function bodyClicked() {
    if (typeof buttonNav.opened == 'undefined') {
        return;
    }
    if (buttonNav.opened) {
        closeNav();
    }
}

function format(d) {
    console.log(d);
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Full name:</td>' +
        '<td>' + d.Input + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Extension number:</td>' +
        '<td>' + d.Startup + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Extra info:</td>' +
        '<td>And any further details here (images etc)...</td>' +
        '</tr>' +
        '</table>';
}


function checkboxes() {

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


}

function rowclick() {
    $("#frametable tbody").on("click", (e) => {
        let tr = $(this).closest('tr');
        let row = APP.FrameTable.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
}

const LOG = (...args) => { console.log(args); };
const ASSERT = (...args) => { console.assert(args); };
const LOG_IF = (expression, ...args) => { if ((expression)) console.log(args); };

function setActive(e) {
    let li = e.currentTarget.parentElement.children;
    for (var i = 0; i < li.length; i++) {
        li[i].children[0].className = "";
    }
    e.currentTarget.children[0].className = "active";
}

$(document).ready(function() {
    APP.InitializeSideBar();
    APP.InitializeDataTable();
    let navs = document.getElementById("navButtons").children;
    for (var i = 0; i < navs.length; i++) {
        navs[i].addEventListener('click', setActive);
    }

});