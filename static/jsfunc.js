$(document).ready(function(){
    $('[data-toggle="popover"]').popover();   
});

// A function to hide devices that dont have the search term in them.
function searchDevices(startCol, endCol, returnedCOl) {
  var input, filter, table, tr, td, i, j, rowTds, array = [], rowString, endCol, startCol, returnedCOl, tret;
  input = document.getElementById("deviceName");
  filter = input.value.toUpperCase();
  table = document.getElementById("deviceTable");
  avalible = document.getElementById("aviable");
  tr = table.getElementsByTagName("tr");
  if (avalible.checked){
    for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    tret = tr[i].getElementsByTagName("td")[returnedCOl];
    // Loop through all the columns of the row and make an array of the them all
    if (tret) {
      if (tret.innerHTML !== '0') {  
        if (td) {
        for (j = startCol; j < endCol; j++) {
          rowTds = tr[i].getElementsByTagName("td")[j].innerHTML;
          array.push(rowTds);
          }
        // Make the row a single string
        rowString = array.toString();
        // Set style to hidden if search term not found
        if (rowString.toUpperCase().search(filter) > -1) {
          tr[i].style.display = "";
          } else {
          tr[i].style.display = "none";
          }
          array = []
          }
        } else {
          tr[i].style.display = "none";
          }
    } else {
      if (td) {
        for (j = startCol; j < endCol; j++) {
          rowTds = tr[i].getElementsByTagName("td")[j].innerHTML;
          array.push(rowTds);
          }
        // Make the row a single string
        rowString = array.toString();
        // Set style to hidden if search term not found
        if (rowString.toUpperCase().search(filter) > -1) {
          tr[i].style.display = "";
          } else {
          tr[i].style.display = "none";
          }
          array = []
        }       
      }
    }
  } else {
  // Loop through all the rows of the table
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    // Loop through all the columns of the row and make an array of the them all
    if (td) {
        for (j = startCol; j < endCol; j++) {
        rowTds = tr[i].getElementsByTagName("td")[j].innerHTML;
        array.push(rowTds);
        }
      // Make the row a single string
      rowString = array.toString();
      // Set style to hidden if search term not found
      if (rowString.toUpperCase().search(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
      array = []
     }       
    }
  }
}    

function sortTable(row) {
  var table, rows, switching, i, x, y, shouldSwitch, row;
  table = document.getElementById("deviceTable");
  switching = true;
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[row];
      y = rows[i + 1].getElementsByTagName("TD")[row];
      //check if the two rows should switch place:
      if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
        //if so, mark as a switch and break the loop:
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

function showEdit() {
    var x = document.getElementById("editUser");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function showStaff() {
    var x = document.getElementById("editStaff");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}
