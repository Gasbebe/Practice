```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>test</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="baatWizard.css">
        <link rel="stylesheet" href="animation/headShake.css">
        <script type="module" src="/node_modules/@vscode/webview-ui-toolkit/dist/toolkit.js"></script>
    </head>
    <body bgcolor="black">
        <div>
            <h1 bgcolor="red">Baat Wizard</h1>
        </div>
        <!-- <vscode-panels activeid="tab-4" aria-label="With Active Tab">
            <vscode-panel-tab id="tab-1">PROBLEMS</vscode-panel-tab>
            <vscode-panel-tab id="tab-2">OUTPUT</vscode-panel-tab>
            <vscode-panel-tab id="tab-3">DEBUG CONSOLE</vscode-panel-tab>
            <vscode-panel-tab id="tab-4">TERMINAL</vscode-panel-tab>
            <vscode-panel-view id="view-1">
                Problems Content
            </vscode-panel-view>
            <vscode-panel-view id="view-2">
                Output Content
            </vscode-panel-view>
            <vscode-panel-view id="view-3">
                Debug Console Content
            </vscode-panel-view>
            <vscode-panel-view id="view-4">
                Terminal Content
                </vscode-panel-view>
        </vscode-panels> -->
        <!-- <script src="" async defer></script> -->
        <!-- <button>my sheet</button> -->
        <vscode-button id="howdy">Howdy!</vscode-button>
        <!-- <vscode-checkbox id="baz">Label</vscode-checkbox> -->
        <vscode-button>cancle</vscode-button>
        <br/>

        <vscode-divider role="presentation"></vscode-divider>
        <br/>

        
        <div calss="headShake" >
            <vscode-badge>general</vscode-badge>
            <vscode-text-field>platform</vscode-text-field>
            <vscode-text-field>application</vscode-text-field>
            <vscode-text-field>version</vscode-text-field>
            <vscode-text-field>full-version</vscode-text-field>
            <vscode-text-field>executable</vscode-text-field>
            <vscode-text-field>namespace</vscode-text-field>
            <vscode-text-field>class-prefix</vscode-text-field>
            <vscode-text-field>main-source</vscode-text-field>
        </div>

        <vscode-divider role="presentation"></vscode-divider>
        <br/>


        <div calss="baatwizard-general">
            <vscode-text-field>folder</vscode-text-field>
            <vscode-text-field>file</vscode-text-field>
            <vscode-text-field>testing</vscode-text-field>
            <vscode-text-field>track-group</vscode-text-field>
            <vscode-text-field>message-group</vscode-text-field>
        </div>

        <vscode-divider role="presentation"></vscode-divider>
        <br/>


        <div>
            <vscode-text-field>service</vscode-text-field>
            <vscode-divider role="presentation"></vscode-divider>
            <br/>
        </div>
        

        <div class="hello">
            <h1>test</h1>
            <vscode-badge>
                1111
            </vscode-badge>
            <vscode-text-field>message-group</vscode-text-field>
        </div>
        <br/>
        <!-- <vscode-text-area>test</vscode-text-area> -->
        <vscode-text-field>test</vscode-text-field>
        <vscode-text-field>test</vscode-text-field>
        <vscode-text-field>test</vscode-text-field>
        <vscode-text-field>test</vscode-text-field>
        <vscode-text-field>test</vscode-text-field>
        <!-- <vscode-dropdown>test</vscode-dropdown> -->

        <!-- Note: Using Visual Studio Code Codicon Library -->

        <vscode-text-field>
	        Text Field Label
	        <!-- <span slot="end" class="codicon codicon-text-size"></span> -->
        </vscode-text-field>
        <vscode-divider role="presentation"></vscode-divider>

        
        <vscode-text-area resize="both" class="baat">Text Area Label</vscode-text-area>

        <script src="test.js"></script>
    </body>
    <footer>testsfdsfdsfdsf</footer>
</html>
```

```
const test1 = 1;
let  web = 1;

const test11 = "test";

const week = ["mon", "tuye", "web"];
const nonsence = ["mon", "tuye", "web", 1, 2];

console.log(week[2]);

function sayHello(){
    console.log("hello!");
}

sayHello();

const player = {
    name : "nico",
    age : 1
};

const player2 = {
    name : "nico",
    age : 1,
    sayHello2: function()
    {
        console.log("player : Hello!");
    }
};

function ftest(param)
{
    console.log(param + 5);
}

ftest(10,1,1,1,1,1,1,1,1);

function myCal(param)
{
    return param + 2;
}

parseInt("15");
if(isNaN(parseInt("15")))
{
    console.log("is NaN");
}

const title = document.getElementById("title");
// title.innerText = "GOOD";

const hellos = document.getElementsByClassName("hello");

const title2 = document.querySelector(".hello h1");
const titleAll = document.querySelectorAll(".hello h1");
const title3 = document.querySelectorAll(".hello h1:first-child");

// getElementById >> 하나의 값
// getElementsByClassName >> 배열
// getElementsByTagName . . . >> 배열
const idTest = document.querySelector("#hello"); //동일 하위 엘리먼트를 가져옴
const idTest2 = document.getElementById("hello"); //동일 하위 엘리먼트를 못가져옴


const idTest22 = document.querySelector("#hello form");

const test32 = document.querySelector("div h1");
//----------------------------------------------------

// const event1 = document.querySelector("div.hello:first-child h1");
// const event1 = document.querySelector("div.hello:first-child h1");
const event1 = document.querySelector(".hello vscode-text-field");
const event2 = document.querySelector(".hello h1");

event1.value = "HELLO";

function readTextFile(file)
{
    let result = "";
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status === 0)
            {
                result = rawFile.responseText;
                return result;
                //alert(allText);
            }
        }
    };
    rawFile.send(null);
    return result;
}

function clickTest()
{
    console.log("click");
}

event1.addEventListener("click", clickTest);

const baatXml = readTextFile("/baat/test.baat.xml");
const parser = new DOMParser();
let xmlText = parser.parseFromString(baatXml, "text/xml");
xmlText.querySelectorAll("SERVICE_GROUP");
console.log(xmlText.querySelectorAll("SERVICE_GROUP"));
```
