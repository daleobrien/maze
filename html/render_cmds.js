
var QUARTER = Math.PI/2;
var HALF = Math.PI;
var THREE_QUARTER  = 3*Math.PI/2;
var FULL = 2*Math.PI;

function s_shape_00(p, x, y, draw_with_curves, a, b, s){
    p.moveTo(x+a, y);
    if (draw_with_curves){
        p.arc(x, y, a, 0, QUARTER, false);
    } else {
        p.lineTo(x+a, y+a);
    }
    p.lineTo(x, y+a);
}

function s_shape_01(p, x, y, draw_with_curves, a, b, s){
    p.moveTo(x, y+b);
    if (draw_with_curves){
        p.arc(x, y+s, a, THREE_QUARTER, 0, false);
    } else {
        p.lineTo(x+a, y+b);
    }
    p.lineTo(x+a, y+s);
}

function s_shape_10(p, x, y, draw_with_curves, a, b, s){

    p.moveTo(x+s, y+a);
    if (draw_with_curves){
        p.arc(x+s, y, a, QUARTER, HALF, false);
    } else {
        p.lineTo(x+b, y+a);
    }
    p.lineTo(x+b, y);
}

function s_shape_11(p, x, y, draw_with_curves, a, b, s){
    p.moveTo(x+s, y+b);
    if (draw_with_curves){
        p.arc(x+s, y+s, a, THREE_QUARTER, HALF, true);
    } else {
        p.lineTo(x+b, y+b);
    }
    p.lineTo(x+b, y+s);
}

function c3(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // │ │
    // │ │

    p.moveTo(x+a, y+s);
    p.lineTo(x+a, y);
    p.moveTo(x+b, y+s);
    p.lineTo(x+b, y);
}

// arc(x+x, y, radius, startAngle, endAngle, anticlockwise)

function c1(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // │ │
    // └─┘
    
    p.moveTo(x+b, y);
    if (draw_with_curves){

        p.lineTo(x+b, y+q);

        p.arc(x + s - v, y + n + r, r, HALF, HALF + delta, true);
        p.arc(x + s / 2, y + s / 2 , s / 2 - g / 2,  theta - QUARTER ,  THREE_QUARTER -  theta, false);

        p.arc(x + v, y + n + r,
              r, QUARTER - theta, THREE_QUARTER + theta - delta, true);

    } else {
        p.lineTo(x+b, y+b);
        p.lineTo(x+a, y+b);
    }
    p.lineTo(x+g, y)

}

function c2(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

      // ┌─┐
      // │ │

    p.moveTo(x+b, y+s);
    if( draw_with_curves){

        p.arc(x + s - v, y + s - n - r, r, HALF, HALF - delta, false);
        p.arc(x+s / 2, y + s / 2 , s / 2 - g / 2, QUARTER - theta ,  theta - THREE_QUARTER, true);
        p.arc(x + v, y + s - n - r, r, THREE_QUARTER + theta, THREE_QUARTER + theta - delta, false);

    } else {
        p.lineTo(x+b, y+a);
        p.lineTo(x+a, y+a);
    }
    p.lineTo(x+a, y+s);

}

function c4(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){


    // ┌──
    // └──

    p.moveTo(x+s, y+b);

    if(draw_with_curves){
        p.arc(x + s - n - r, y + s - v, r, THREE_QUARTER, THREE_QUARTER + delta, true);
        p.arc(x+s / 2, y + s / 2 , s / 2 - g / 2, QUARTER + delta ,  QUARTER + delta - 2 * theta , false);
        p.arc(x + s - n - r, y + v, r, HALF - theta, HALF - theta + delta, true);

    }else{
        p.lineTo(x+g, y+b);
        p.lineTo(x+a, y+a);
    }
    p.lineTo(x+s, y+a);

}

function c8(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

  // ──┐
  // ──┘

    p.moveTo(x, y+b);
    if( draw_with_curves ){
        p.arc(x + n + r, y + s - v, r, THREE_QUARTER, THREE_QUARTER - delta, false);
        p.arc(x + s / 2, y + s / 2 , s / 2 - g / 2, QUARTER - delta ,  QUARTER - delta + 2 * theta , true);
        p.arc(x + n + r, y + v, r, theta , theta - delta, false);

    } else { 
        p.lineTo(x+b, y+b);
        p.lineTo(x+b, y+a);
    }
    p.lineTo(x, y+a);

}

function c5(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    //  │ └
    //  └──
    //
    s_shape_10(p, x, y, draw_with_curves, a, b, s);

    p.moveTo(x+s, y+b);
    if( draw_with_curves){
        if(start) {
            p.arc(x+(a + b) / 2, y+(a + b) / 2, (b - a) / 2, QUARTER , HALF, false);
            
        } else {
            p.arc(x+b, y+a, b - a, QUARTER , HALF, false);
        }
    } else {
        p.lineTo(x+a, y+b);
    }
    p.lineTo(x+a, y);
}

function c6(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ┌──
    // │ ┌

    s_shape_11(p, x, y, draw_with_curves, a, b, s);

    p.moveTo(x+s, y+a);
    if( draw_with_curves){
        p.arc(x+a + b, y+a + b, b, THREE_QUARTER , HALF, true);
    } else{
        p.lineTo(x+a, y+a);
    }
    p.lineTo(x+a, y+s);


}

function c9(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){


    //  ┘ │
    //  ──┘

    s_shape_00(p, x, y, draw_with_curves, a, b, s);

    p.moveTo(x+b, y);
    if( draw_with_curves){
        p.arc(x+a, y+a, b - a, 0 , QUARTER, false);
    } else {
        p.lineTo(x+b, y+b);
    }
    p.lineTo(x, y+b);


}

function c10(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ──┐
    // ┐ │

    s_shape_01(p, x, y, draw_with_curves, a, b, s);

    p.moveTo(x, y+a);
    if(draw_with_curves){
        if(end){
            p.arc(x+(a + b) / 2, y + (a + b) / 2, (b - a) / 2, THREE_QUARTER , FULL, false);
        }else{
            p.arc(x+a, y+ b, b - a, THREE_QUARTER , FULL, false);
        }
    }else{
        p.lineTo(x+b, y+a);
    }
    p.lineTo(x+b, y+s);

}

function c7(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // │ └
    // │ ┌

    p.moveTo(x+a, y+s);
    p.lineTo(x+a, y);

    s_shape_10(p, x, y, draw_with_curves, a, b, s);
    s_shape_11(p, x, y, draw_with_curves, a, b, s);
}

function c11(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

     // ┘ │
     // ┐ │

    p.moveTo(x+b, y+s);
    p.lineTo(x+b, y);

    s_shape_00(p, x, y, draw_with_curves, a, b, s);
    s_shape_01(p, x, y, draw_with_curves, a, b, s);
}


function c13(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ┘ └
    // ───

    p.moveTo(x, y+b);
    p.lineTo(x+s, y+b);

    s_shape_00(p, x, y, draw_with_curves, a, b, s);
    s_shape_10(p, x, y, draw_with_curves, a, b, s);
}

function c14(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ───
    // ┐ ┌

    p.moveTo(x, y+a);
    p.lineTo(x+s, y+a);

    s_shape_01(p, x, y, draw_with_curves, a, b, s);
    s_shape_11(p, x, y, draw_with_curves, a, b, s);
}

function c15(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ┘ └
    // ┐ ┌

    s_shape_00(p, x, y, draw_with_curves, a, b, s);
    s_shape_01(p, x, y, draw_with_curves, a, b, s);
    s_shape_10(p, x, y, draw_with_curves, a, b, s);
    s_shape_11(p, x, y, draw_with_curves, a, b, s);

}

function c12(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ───
    // ───

    p.moveTo(x, y+b);
    p.lineTo(x+s, y+b);
    p.moveTo(x, y+a);
    p.lineTo(x+s, y+a);
}

function c19(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ┤ ├
    // ┤ ├

    p.moveTo(x+a, y+s);
    p.lineTo(x+a, y);
    p.moveTo(x+b, y+s);
    p.lineTo(x+b, y);

    p.moveTo(x, y+a);
    p.lineTo(x+a, y+a);
    p.moveTo(x, y+b);
    p.lineTo(x+a, y+b);

    p.moveTo(x+s, y+a);
    p.lineTo(x+b, y+a);
    p.moveTo(x+s, y+b);
    p.lineTo(x+b, y+b);
}

function c28(p, x, y, draw_with_curves, a, b, g, n, r, s, q, v, delta, theta, start, end){

    // ┴─┴
    // ┬─┬

    p.moveTo(x, y+b);
    p.lineTo(x+s, y+b);
    p.moveTo(x, y+a);
    p.lineTo(x+s, y+a);

    p.moveTo(x+a, y+a);
    p.lineTo(x+a, y);
    p.moveTo(x+a, y+b);
    p.lineTo(x+a, y+s);

    p.moveTo(x+b, y+a);
    p.lineTo(x+b, y);
    p.moveTo(x+b, y+b);
    p.lineTo(x+b, y+s);

}
