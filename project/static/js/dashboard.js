let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".sidebarBtn");
sidebarBtn.onclick = function () {
  sidebar.classList.toggle("active");
  if (sidebar.classList.contains("active")) {
    sidebarBtn.classList.replace("bx-menu", "bx-menu-alt-right");
  } else sidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
};


function profileToggle(){
    const toggleProfile = document.querySelector('.profile_dd')
    toggleProfile.classList.toggle('active')
}

function notificationToggle(){
    const toggleNotification = document.querySelector('.notification_dd')
    toggleNotification.classList.toggle('active')
}


