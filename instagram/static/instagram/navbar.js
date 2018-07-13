function ShowNavbar()
{
    document.getElementById("navbarid").style.zIndex = 1;
    document.getElementById("navbuttonid").style.zIndex = -1;
    document.getElementById("hidenavbarid").style.zIndex = -1;
}

function HideNavbar()
{
    document.getElementById("navbarid").style.zIndex = -1;
    document.getElementById("navbuttonid").style.zIndex = 1;
    document.getElementById("hidenavbarid").style.zIndex = 1;
}