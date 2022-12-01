import uuid
import os
import json

class ColorPicker():
    # this will have an additional line prepended
    _bootstrap = """
    var uid = '{uid}';
    var named_colors = {colors};
    var currentFrame = document.querySelector('#ColorPickerShadowRoot_' + uid)
    var shadow = currentFrame.attachShadow({{mode: 'open'}});
    var template = currentFrame.querySelector('#ColorPickerTemplate');
    var clone = document.importNode(template.content, true);
    shadow.appendChild(clone);
    """
    _js = """
    var currentFrame = document.currentScript.parentNode.shadowRoot
    var colorPicker = currentFrame.querySelector('#color_picker');
    colorPicker.addEventListener("input", watchColorPicker, false);
    var colorSelector = currentFrame.querySelector('#color_selector');
    colorSelector.addEventListener("input", watchColorSelector, false);

    var changeEvent = new CustomEvent("input")


    function watchColorPicker(event) {
        var currentWidget = event.target.closest('tbody');
        var rgbcode = currentWidget.querySelector('#rgb_code');
        var hexcode = currentWidget.querySelector('#hex_code');
        var hslcode = currentWidget.querySelector('#hsl_code');
        
        var rgb_val = hexToRgb(event.target.value);
        var hsl_val = rgbToHsl(rgb_val);
        rgbcode.innerHTML = `rgb(${rgb_val.r.toString()}, ${rgb_val.g.toString()}, ${rgb_val.b.toString()})`;
        hslcode.innerHTML = `hsl(${hsl_val.h.toString()}, ${hsl_val.s.toString()}%, ${hsl_val.l.toString()}%)`;
        hexcode.innerHTML = event.target.value;

        var bgs = currentWidget.querySelectorAll(".color_bg"),
            txts = currentWidget.querySelectorAll(".color_text");

        for (var i=0; i < bgs.length; i++) {
            bgs[i].style.backgroundColor = event.target.value;
            var lbl = currentWidget.querySelector('#input_label')
            adjustColor(lbl, hsl_val)
        }

        for (var i=0; i < txts.length; i++) {
            txts[i].style.color = event.target.value;
        }

        populateHslTable(hsl_val, currentWidget);
        populateColorTable(hsl_val, currentWidget);

        closerNamedColors = findCloserColors(xyzToLab(rgbToXyz(rgb_val)));

        sg_el_index = 1
        for (var i=0; i < 5; i++) {
            if (named_colors[closerNamedColors[i]] == event.target.value) {
                continue
            }

            sg_el = currentWidget.querySelector('#suggested_colors' + sg_el_index.toString())
            sg_el.innerHTML = closerNamedColors[i];
            sg_el.style.backgroundColor = named_colors[closerNamedColors[i]];
            adjustColor(sg_el, rgbToHsl(hexToRgb(named_colors[closerNamedColors[i]])));
            sg_el_index ++
        }

    }

    function watchColorSelector(event) {
        var validColor = isValidColor(event.target.value)
        var isNamedColor = event.target.value in named_colors
        if(validColor != '' || isNamedColor) {
            var currentWidget = event.target.closest('tbody');
            var picker = currentWidget.querySelector('#color_picker');
            
            rgb_val = digestRGBCode(validColor);
            if(rgb_val == null){
                hex_code = colourNameToHex(event.target.value);
            } else {
                hex_code = rgbToHex(rgb_val);
            }

            if(hex_code != false) {
                picker.value = hex_code;
                picker.dispatchEvent(changeEvent);
            }

        } 
    }

    function isValidColor(strColor) {
        switch(strColor) {
            case "unset":
            case "inherit":
            case "initial":
                return ''
                break
        }
        var s = new Option().style;
        s.color = strColor;

        // return 'false' if color wasn't assigned
        return s.color;
    }

    function adjustColor(el, hsl) {
        if(hsl.l < 50) {
            el.style.color = 'white'
        } else {
            el.style.color = 'black'
        }
    }

    function populateHslTable(hsl, elParent) {
        var closerLuminance = Math.round(hsl.l/10)*10;

        for(var i = 0; i <= 100; i+=10) {
            var el = elParent.getElementsByClassName(i.toString()+'perc')[0];
            var tempHSL = JSON.parse(JSON.stringify(hsl));

            tempHSL.l = i;
            el.classList.remove('active');
            el.style.backgroundColor = `hsl(${tempHSL.h.toString()}, ${tempHSL.s.toString()}%, ${tempHSL.l.toString()}%)`;
            adjustColor(el, tempHSL)

            el.innerHTML = i.toString() + '% ' + rgbToHex(hslToRgb(tempHSL));
        }

        var el = elParent.getElementsByClassName(closerLuminance.toString()+'perc')[0];
        el.classList.add('active');
    }

    function formatColorSection(el, hsl) {
        el.style.backgroundColor = `hsl(${hsl.h.toString()}, ${hsl.s.toString()}%, ${hsl.l.toString()}%)`;
        adjustColor(el, hsl);

        var label = /(\([\w]+\)).*/.exec(el.innerHTML);
        el.innerHTML = label[1] + ' ' + rgbToHex(hslToRgb(hsl));
    }

    function populateColorTable(hsl, elParent) {
        var el = elParent.getElementsByClassName('analogue1')[0];
        var tempHSL = JSON.parse(JSON.stringify(hsl));
        tempHSL.h = (hsl.h + 30) % 360;
        formatColorSection(el, tempHSL);

        var el = elParent.getElementsByClassName('analogue2')[0];
        var tempHSL = JSON.parse(JSON.stringify(hsl));
        tempHSL.h = (hsl.h - 30) % 360;
        tempHSL.h = tempHSL.h < 0 ? tempHSL.h + 360 : tempHSL.h
        formatColorSection(el, tempHSL);

        var el = elParent.getElementsByClassName('complementary')[0];
        var tempHSL = JSON.parse(JSON.stringify(hsl));
        tempHSL.h = (hsl.h + 180) % 360;
        formatColorSection(el, tempHSL);

        var el = elParent.getElementsByClassName('triadic1')[0];
        var tempHSL = JSON.parse(JSON.stringify(hsl));
        tempHSL.h = (hsl.h + 120) % 360;
        formatColorSection(el, tempHSL);

        var el = elParent.getElementsByClassName('triadic2')[0];
        var tempHSL = JSON.parse(JSON.stringify(hsl));
        tempHSL.h = (hsl.h + 240) % 360;
        formatColorSection(el, tempHSL);

    }

    function copyHexColor(el) {
        console.log('clicked');
        console.log(el);
        var currentWidget = el.closest('tbody');
        console.log(currentWidget);
        var picker = currentWidget.querySelector('#color_picker');
        console.log(picker);

        console.log('clicked2');
        var hex_code = rgbToHex(el.style.backgroundColor);
        console.log(hex_code);
        picker.value = hex_code;
        picker.dispatchEvent(changeEvent);
    }

    function hexToRgb(hex) {
        var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    }

    function componentToHex(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
    }

    function rgbToHex(rgb) {
        if (typeof rgb == 'string' ) {
            rgb = digestRGBCode(rgb);
        }

        var r = componentToHex(rgb.r),
            g = componentToHex(rgb.g),
            b = componentToHex(rgb.b);

        if (r.length != 2) {
            return false
        }
        if (g.length != 2) {
            return false
        }
        if (b.length != 2) {
            return false
        }
        return "#" + r + g + b;
    }

    function digestRGBCode(rgb) {
        var result = /rgb[a]?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)[\s,]*(\d*)\)/.exec(rgb);
        return result ? {
            r: parseInt(result[1]),
            g: parseInt(result[2]),
            b: parseInt(result[3])
        } : null;
    }

    function colourNameToHex(colour)
    {
        if (typeof named_colors == 'undefined') {
            return false;
        }

        if (typeof named_colors[colour.toLowerCase()] != 'undefined')
            return named_colors[colour.toLowerCase()];

        return false;
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

    function rgbToXyz(rgb){
        var r = parseFloat(rgb.r / 255 ),
            g = parseFloat(rgb.g / 255 ),       //G from 0 to 255
            b = parseFloat(rgb.b / 255 )        //B from 0 to 255

        if ( r > 0.04045 ) r = Math.pow( (( r + 0.055 ) / 1.055 ), 2.4)
        else                   r = r / 12.92
        if ( g > 0.04045 ) g = Math.pow( (( g + 0.055 ) / 1.055 ), 2.4)
        else                   g = g / 12.92
        if ( b > 0.04045 ) b = Math.pow( (( b + 0.055 ) / 1.055 ), 2.4)
        else                   b = b / 12.92

        r = r * 100
        g = g * 100
        b = b * 100

        //Observer. = 2°, Illuminant = D65
        return {
            x: r * 0.4124 + g * 0.3576 + b * 0.1805,
            y: r * 0.2126 + g * 0.7152 + b * 0.0722,
            z: r * 0.0193 + g * 0.1192 + b * 0.9505
        };
    }


    function xyzToLab(xyz) {
        const ref_X =  95.047,
              ref_Y = 100.000,
              ref_Z = 108.883;

        var x = xyz.x / ref_X,          //ref_X =  95.047   Observer= 2°, Illuminant= D65
            y = xyz.y / ref_Y,          //ref_Y = 100.000
            z = xyz.z / ref_Z;          //ref_Z = 108.883

        if ( x > 0.008856 ) x = Math.pow(x, ( 1/3 ))
        else                    x = ( 7.787 * x ) + ( 16 / 116 )
        if ( y > 0.008856 ) y = Math.pow(y, ( 1/3 ))
        else                    y = ( 7.787 * y ) + ( 16 / 116 )
        if ( z > 0.008856 ) z = Math.pow(z, ( 1/3 ))
        else                    z = ( 7.787 * z ) + ( 16 / 116 )

        return {
            l: ( 116 * y ) - 16,
            a: 500 * ( x - y ),
            b: 200 * ( y - z )
        }
    }

    var named_color_lab = { }
    for (const [key, value] of Object.entries(named_colors)) {
        named_color_lab[key] = xyzToLab(rgbToXyz(hexToRgb(value)))
    }

    // https://stackoverflow.com/questions/46622486/what-is-the-javascript-equivalent-of-numpy-argsort
    var argsort = (arr1, arr2) => arr1
        .map((item, index) => [arr2[index], item]) // add the args to sort by
        .sort(([arg1], [arg2]) => arg2 - arg1) // sort by the args
        .map(([, item]) => item); // extract the sorted items

    function findCloserColors(target_labColor, n_colors=5) {
        var colorDistance = { }
        for (const [key, value] of Object.entries(named_color_lab)) {
            colorDistance[key] = Math.sqrt( Math.pow(target_labColor.l - value.l, 2) + Math.pow(target_labColor.a - value.a, 2) + Math.pow(target_labColor.b - value.b, 2) )
        }

        closerColors = argsort(Object.keys(colorDistance), Object.values(colorDistance))
        return closerColors.slice(-n_colors).reverse()
    }

    colorPicker.dispatchEvent(changeEvent)
    """

    _style = """
        table {
            width:80%;
            border-collapse: collapse;
            border-spacing: 0;
            color: var(--jp-ui-font-color1);
            }
        thead {
            border-bottom: 1px solid white;
            }

        td {
            padding: 0 !important;
            vertical-align: middle;
            width: 30%;
            height: 30px;
            border-radius: 3px;
            }
        td > p {
            height: 30px;
            transition: transform 0.3s;
            height: 90%;
            border-radius: 3px;
        }
        .complementary:hover,
        .analogue1:hover,
        .analogue2:hover,
        .triadic1:hover,
        .triadic2:hover,
        #suggested_colors1:hover,
        #suggested_colors2:hover,
        #suggested_colors3:hover,
        #suggested_colors4:hover {
            transform: scale(0.96);
        }
        #color_selector {
            display: block;
            margin: auto;
            width: 80%;
            height: 25px;
        }
        #input_label {
            position: absolute;
            width: 50%;
            height: 50%;
            top: 25%;
            left: 25%;
            z-index: 99;
            line-height: normal;
            pointer-events: none;
            }
        p   {
            margin:0 !important;
            text-align: center !important;
            font-weight: bold;
            }
        .hsl_cell > div {
            width: 80%;
            height: 90%;
            text-align:center;
            margin: auto;
            transition: transform 0.3s;
            border-radius: 3px;
            }
        .hsl_cell >div:hover {
            transform: scale(0.96);
        }
        .hsl_cell {
            height:30px;
            line-height:30px;
            }
        .active {
            height:45px !important;
            line-height:45px !important;
            }
    """

    _layout = """
    <script>
    {bootstrap}
    </script>

    <div id='ColorPickerShadowRoot_{uid}'>
        <script>
        {js}
        </script>
        <template id='ColorPickerTemplate'>

            <style>
            {css}
            </style>

            <table>
                <thead><tr>
                        <td colspan=6 style='text-align:center;'>Color Picker</td>
                </tr></thead>
                <tbody>

                    <tr colspan=6>
                        <td colspan=2 rowspan=4 style="padding:0 20px !important; position:relative;">
                            <input type="color" id="color_picker" name="color_picker"
                                value="#001c2b" style="width:100%; height:100px;">
                            <p id='input_label'>Pick a color or type a color code below</p>
                        </td>
                        <td colspan=2 rowspan=1 class='empty'></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="0perc" onclick='copyHexColor(this)'>0%</div></td>
                    </tr>
                    <tr>
                        <td colspan=2 rowspan=1 class='color_bg' ><p  style='color: black;' >black text</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="10perc" onclick='copyHexColor(this)'>10%</div></td>
                    </tr>
                    <tr>
                        <td colspan=2 rowspan=1 class='color_bg' ><p style='color:white;'>white text</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="20perc" onclick='copyHexColor(this)'>20%</div></td>
                    </tr>
                    <tr>
                        <td colspan=2 rowspan=1 style='background-color:black;'><p class='color_text' >colored text</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="30perc" onclick='copyHexColor(this)'>30%</div></td>
                    </tr>

                    <tr colspan=6>
                        <td colspan=2 rowspan=1 class='empty'></td>
                        <td colspan=2 rowspan=1 style='background-color:white;'><p class='color_text' >colored text</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="40perc" onclick='copyHexColor(this)'>40%</div></td>
                    </tr>

                    <tr colspan=6>
                        <td colspan=2 rowspan=1>
                            <input type="text" id="color_selector" name="color_selector"
                                    placeholder="(e.g. csiro_darkblue, gold, rgb(..), hsl(..), #..">
                        </td>
                        <td colspan=2 rowspan=1><p class="analogue1" onclick='copyHexColor(this)'>(analogue)</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="50perc" onclick='copyHexColor(this)'>50%</div></td>
                    </tr>

                    <tr colspan=6>
                        <td colspan=2 rowspan=1 class='empty'></td>
                        <td colspan=2 rowspan=1><p class="analogue2" onclick='copyHexColor(this)'>(analogue)</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="60perc" onclick='copyHexColor(this)'>60%</div></td>
                    </tr>

                    <tr colspan=6>
                        <td colspan=2 rowspan=1><p class='value_element' id='rgb_code'>rbg(0, 0, 0)</p></td>
                        <td colspan=2 rowspan=1><p class="complementary" onclick='copyHexColor(this)'>(complementary)</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="70perc" onclick='copyHexColor(this)'>70%</div></td>
                    </tr>

                    <tr colspan=6>
                        <td colspan=2 rowspan=1><p class='value_element' id='hsl_code'>hsl(0, 0%, 0%)</p></td>
                        <td colspan=2 rowspan=1><p class="triadic1" onclick='copyHexColor(this)'>(triadic)</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="80perc" onclick='copyHexColor(this)'>80%</div></td>
                    </tr>

                    <tr colspan=6>
                        <td colspan=2 colspan=1 rowspan=1><p class='value_element' id='hex_code'>#000000</p></td>
                        <td colspan=2 rowspan=1><p class="triadic2" onclick='copyHexColor(this)'>(triadic)</p></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="90perc" onclick='copyHexColor(this)'>90%</div></td>
                    </tr>

                    <tr colspan=6>
                        <td colspan=2 rowspan=1 class='empty'></td>
                        <td colspan=2 rowspan=1 class='empty'></td>
                        <td colspan=2 rowspan=1 class='hsl_cell'><div class="100perc" onclick='copyHexColor(this)'>100%</div></td>
                    </tr>
                    <tr colspan=6>
                        <td colspan=2 rowspan=1 class='value_element'>
                            <p class='value_element'>Suggested Named Colors</p>
                        </td>
                        <td colspan=4 rowspan=1 class='value_element'>
                            <p class='value_element' id='suggested_colors1' onclick='copyHexColor(this)' style="width:23%; display:inline-block">Suggested Named Colors</p>
                            <p class='value_element' id='suggested_colors2' onclick='copyHexColor(this)' style="width:23%; display:inline-block">Suggested Named Colors</p>
                            <p class='value_element' id='suggested_colors3' onclick='copyHexColor(this)' style="width:23%; display:inline-block">Suggested Named Colors</p>
                            <p class='value_element' id='suggested_colors4' onclick='copyHexColor(this)' style="width:23%; display:inline-block">Suggested Named Colors</p>
                        </td>
                    </tr>

                </tbody>
            </table>
        </template>
    </div>
    """

    NAMED_COLORS = json.load(open(os.path.join(os.path.dirname(__file__), './named_colors.json')))

    def __init__(self):
        pass

    def _repr_html_(self):

        uid = uuid.uuid4().hex
        _bootstrap = self._bootstrap.format(uid=str(uid), colors=json.dumps(self.NAMED_COLORS))

        return self._layout.format(uid=uid, js=self._js, bootstrap=_bootstrap, css=self._style)

colorPicker = ColorPicker()