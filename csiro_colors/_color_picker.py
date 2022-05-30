from IPython.display import HTML

_js = """
var colorPicker = document.getElementById('color_picker');
colorPicker.addEventListener("input", watchColorPicker, false);

function watchColorPicker(event) {
    var rgbcode = document.getElementById('rgb_code');
    var hexcode = document.getElementById('hex_code');
    var hslcode = document.getElementById('hsl_code');
    
    var rgb_val = hexToRgb(event.target.value);
    var hsl_val = rgbToHsl(rgb_val);
    rgbcode.innerHTML = `rgb(${rgb_val.r.toString()}, ${rgb_val.g.toString()}, ${rgb_val.b.toString()})`;
    hslcode.innerHTML = `hsl(${hsl_val.h.toString()}, ${hsl_val.s.toString()}%, ${hsl_val.l.toString()}%)`;
    hexcode.innerHTML = event.target.value;

    var bgs = document.getElementsByClassName("color_bg"),
        txts = document.getElementsByClassName("color_text");

    Array.prototype.forEach.call(bgs, function(p) {
        p.style.backgroundColor = event.target.value;
        var lbl = document.getElementById('input_label')
        adjustColor(lbl, hsl_val)
    })

    Array.prototype.forEach.call(txts, function(p) {
        p.style.color = event.target.value;
        populateHslTable(hsl_val)
    })
}

function adjustColor(el, hsl) {
    if(hsl.l < 50) {
        el.style.color = 'white'
    } else {
        el.style.color = 'black'
    }
}

function populateHslTable(hsl) {
    var closerLuminance = Math.round(hsl.l/10)*10;

    for(var i = 0; i <= 100; i+=10) {
        var el = document.getElementById(i.toString()+'perc');
        var tempHSL = JSON.parse(JSON.stringify(hsl));;

        tempHSL.l = i;
        el.classList.remove('active');
        el.style.backgroundColor = `hsl(${tempHSL.h.toString()}, ${tempHSL.s.toString()}%, ${tempHSL.l.toString()}%)`;
        adjustColor(el, tempHSL)
    }

    var el = document.getElementById(closerLuminance.toString()+'perc');
    el.classList.add('active');
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function rgbToHsl(rgb){
    var r = rgb.r/255,
        g = rgb.g/255,
        b = rgb.b/255;

    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, l = (max + min) / 2;

    if(max == min){
        h = s = 0; // achromatic
    } else {
        var d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return {
        h: Math.floor(h * 360),
        s: Math.floor(s * 100),
        l: Math.floor(l * 100)
    }

}

function hslToRgb(hsl){
    const h = hsl.h / 360, s = hsl.s / 100, l = hsl.l / 100;
    var r, g, b;

    if(s == 0){
        r = g = b = l; // achromatic
    }else{
        var hue2rgb = function hue2rgb(p, q, t){
            if(t < 0) t += 1;
            if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        }

        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }

    return {
        r: parseInt(Math.round(r * 255)),
        g: parseInt(Math.round(g * 255)),
        b: parseInt(Math.round(b * 255))
    };
}

var event = new CustomEvent("input")
colorPicker.dispatchEvent(event)
"""

_style = """
    td {
        padding: 0 !important;
        vertical-align: middle;
        }
    #input_label {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: 99;
        line-height: 150px;
        pointer-events: none;
        }
    p   {
        margin-bottom:0 !important;
        text-align: center !important;
        font-weight: bold;
        }
    .hsl_cell > div {
        width: 80%;
        height: 90%;
        text-align:center;
        margin: auto;
        }
    .hsl_cell {
        height:25px;
        line-height:25px;
        }
    .active {
        height:40px !important;
        line-height:40px !important;
        }
"""


_layout = """
<script>
{0}
</script>

<style>
{1}
</style>

<table>
    <thead><tr>
            <td colspan=4 style='text-align:center;'>Color Picker</td>
    </tr></thead>
    <tbody>
        <tr colspan=4>
            <td colspan=2 rowspan=5 style="padding:20px !important; position:relative;">
                <input type="color" id="color_picker" name="color_picker"
                    value="#00313C" style="width:96%; height:100px;">
                <p id='input_label'>Select a color using this element</p>
            </td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="empty"></div></td>
        </tr>
        <tr><td colspan=2 rowspan=1 class='hsl_cell'><div id="0perc">0%</div></div></td></tr>
        <tr><td colspan=2 rowspan=1 class='hsl_cell'><div id="10perc">10%</div></td></tr>
        <tr><td colspan=2 rowspan=1 class='hsl_cell'><div id="20perc">20%</div></td></tr>
        <tr><td colspan=2 rowspan=1 class='hsl_cell'><div id="30perc">30%</div></td></tr>
        <tr colspan=4>
            <td colspan=2 rowspan=1><p class='value_element' id='rgb_code'>rbg(0, 0, 0)</p></td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="40perc">40%</div></td>
        </tr>
        <tr colspan=4>
            <td colspan=2 rowspan=1><p class='value_element' id='hsl_code'>hsl(0, 0%, 0%)</p></td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="50perc">50%</div></td>
        </tr>
        <tr colspan=4>
            <td colspan=2 colspan=1 rowspan=1><p class='value_element' id='hex_code'>#000000</p></td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="60perc">60%</div></td>
        </tr>
        <tr colspan=4>
            <td colspan=2 colspan=1 rowspan=1 class='color_bg' ><p  style='color: black;' >black text</p></td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="70perc">70%</div></td>
        </tr>
        <tr colspan=4>
            <td colspan=2 colspan=1 rowspan=1 class='color_bg' ><p style='color:white;'>white text</p></td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="80perc">80%</div></td>
        </tr>
        <tr colspan=4>
            <td colspan=2 colspan=1 rowspan=1 style='background-color:black;'><p class='color_text' >colored text</p></td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="90perc">90%</div></td>
        </tr>
        <tr colspan=4>
            <td colspan=2 colspan=1 rowspan=1 style='background-color:white;'><p class='color_text' >colored text</p></td>
            <td colspan=2 rowspan=1 class='hsl_cell'><div id="100perc">100%</div></td>
        </tr>
    </tbody>
</div>
"""

colorPicker = HTML(_layout.format(_js, _style))