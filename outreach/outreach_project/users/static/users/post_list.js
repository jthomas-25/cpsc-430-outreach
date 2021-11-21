var allLists = document.getElementsByTagName('label');

for(var x = 0; x < allLists.length; x++)
{
    allLists[x].onclick=function()
    {
        if(this.parentNode)
        {
            var childList = this.parentNode.getElementsByClassName('collapsable_content');
            console.log(this.nodeName)

            console.log(this.parentNode)
            console.log(childList)
            for(var y = 0; y< childList.length;y++)
            {
                var currentState = childList[y].style.display;
                if(currentState=="block")
                {
                    childList[y].style.display="none";
                }
                else
                {
                    childList[y].style.display="block";
                }
            }
        }
    }
}
