'use strict';

const π = Math.PI;
const π1_2 = π / 2;
const π3_2 = 3 * π / 2;
const π2 = 2 * π;
const W = ${width};
const H = ${height};
const A = ${a};
const B = ${b};
const G = ${g};
const n = ${n};
const R = ${r};
const S = ${s};
const Q = ${q};
const V = ${v};
const Δ = ${delta};
const θ = ${theta};
${s_x_s};
${s_y_s};

class SVG {
  // Way to generate SVG using the same inteface we used with A JS Canvas
  constructor() {
    this.svg = '';
    this.dots = '';
  }

  path(x, y) {
    return '<path stroke-linecap="round" d="' + this.svg + '  "></path>' +
        this.dots;
  }

  dot(x, y) {
    const _x = x + S / 2;
    const _y = y + S / 2;

    this.dots += '<circle cx="' + _x + '" cy="' + _y + '" r="' + S / 3 +
        '" fill-opacity="1.0" stroke-opacity="0" fill="#E51919" />';
  }

  posAngle(angle) {
    return angle < 0 ? angle + π2 : angle;
  }

  polar(x, y, radius, angle) {
    return {
      x: x + (radius * Math.cos(angle)),
      y: y + (radius * Math.sin(angle))
    };
  }

  a(x, y, radius, startAngle, endAngle, dir = 1) {
    const _start = this.posAngle(startAngle);
    const _end = this.posAngle(endAngle);

    const start = this.polar(x, y, radius, _start);
    const end = this.polar(x, y, radius, _end);

    const diff = _end - _start;
    const largeArcFlag = 0 < diff && diff <= π ? 1 - dir : dir;

    this.svg += [
      'L', start.x.toFixed(2), ' ', start.y.toFixed(2), ' A', radius.toFixed(2),
      ' ', radius.toFixed(2), ' 0 ', largeArcFlag, ' ', dir, ' ',
      end.x.toFixed(2), ' ', end.y.toFixed(2), ' '
    ].join('');
  }

  m(x, y) {
    this.svg += ['M', x.toFixed(2), ' ', y.toFixed(2), ' '].join('');
  };

  l(x, y) {
    this.svg += ['L', x.toFixed(2), ' ', y.toFixed(2), ' '].join('');
  }
}

let p = new SVG();

const s0 =
    (x, y) => {
      p.m(x + A, y);
      p.a(x, y, A, 0, π1_2);
      p.l(x, y + A);
    }

const s1 =
    (x, y) => {
      p.m(x, y + B);
      p.a(x, y + S, A, π3_2, π2);
      p.l(x + A, y + S);
    }

const s2 =
    (x, y) => {
      p.m(x + S, y + A);
      p.a(x + S, y, A, π1_2, π);
      p.l(x + B, y);
    }

const s3 =
    (x, y) => {
      p.m(x + S, y + B);
      p.a(x + S, y + S, A, π3_2, π, 0);
      p.l(x + B, y + S);
    }


const c1 =
    (x, y) => {
      p.m(x + B, y);
      p.l(x + B, y + Q);

      p.a(x + S - V, y + n + R, R, π, π + Δ, 0);

      p.a(x + S / 2, y + S / 2, S / 2 - G / 2, θ - π1_2, π3_2 - θ);

      p.a(x + V, y + n + R, R, π1_2 - θ, π3_2 + θ - Δ, 0);

      p.l(x + G, y);
    }

const c2 =
    (x, y) => {
      p.m(x + B, y + S);
      p.a(x + S - V, y + S - n - R, R, π, π - Δ);
      p.a(x + S / 2, y + S / 2, S / 2 - G / 2, π1_2 - θ, θ - π3_2, 0);
      p.a(x + V, y + S - n - R, R, π3_2 + θ, π3_2 + θ - Δ, 1);

      p.l(x + A, y + S);
    }

const c3 =
    (x, y) => {
      p.m(x + A, y + S);
      p.l(x + A, y);
      p.m(x + B, y + S);
      p.l(x + B, y);
    }

const c4 =
    (x, y) => {
      p.m(x + S, y + B);

      p.a(x + S - n - R, y + S - V, R, π3_2, π3_2 + Δ, 0);
      p.a(x + S / 2, y + S / 2, S / 2 - G / 2, π1_2 + Δ, π1_2 + Δ - 2 * θ);
      p.a(x + S - n - R, y + V, R, π - θ, π - θ + Δ, 0);
      p.l(x + S, y + A);
    }


const c5 =
    (x, y) => {
      s2(x, y);

      p.m(x + S, y + B);
      p.a(x + B, y + A, B - A, π1_2, π);
      p.l(x + A, y);
    }

const c6 =
    (x, y) => {
      s3(x, y);

      p.m(x + S, y + A);
      p.a(x + A + B, y + A + B, B, π3_2, π, 0);
      p.l(x + A, y + S);
    }

const c7 =
    (x, y) => {
      p.m(x + A, y + S);
      p.l(x + A, y);

      s2(x, y);
      s3(x, y);
    }

const c8 =
    (x, y) => {
      p.m(x, y + B);
      p.a(x + n + R, y + S - V, R, π3_2, π3_2 - Δ);
      p.a(x + S / 2, y + S / 2, S / 2 - G / 2, π1_2 - Δ, π1_2 - Δ + 2 * θ, 0);
      p.a(x + n + R, y + V, R, θ, θ - Δ);
      p.l(x, y + A);
    }

const c9 =
    (x, y) => {
      s0(x, y);
      p.m(x + B, y);
      p.a(x + A, y + A, B - A, 0, π1_2);
      p.l(x, y + B);
    }

const ca =
    (x, y) => {
      s1(x, y);
      p.m(x, y + A);
      p.a(x + A, y + B, B - A, π3_2, π2);
      p.l(x + B, y + S);
    }

const cb =
    (x, y) => {
      p.m(x + B, y + S);
      p.l(x + B, y);
      s0(x, y);
      s1(x, y);
    }

const cc =
    (x, y) => {
      p.m(x, y + B);
      p.l(x + S, y + B);
      p.m(x, y + A);
      p.l(x + S, y + A);
    }

const cd =
    (x, y) => {
      p.m(x, y + B);
      p.l(x + S, y + B);
      s0(x, y);
      s2(x, y);
    }

const ce =
    (x, y) => {
      p.m(x, y + A);
      p.l(x + S, y + A);
      s1(x, y);
      s3(x, y);
    }

const cf =
    (x, y) => {
      s0(x, y);
      s1(x, y);
      s2(x, y);
      s3(x, y);
    }



const cg =
    (x, y) => {
      p.m(x + A, y + S);
      p.l(x + A, y);
      p.m(x + B, y + S);
      p.l(x + B, y);

      p.m(x, y + A);
      p.l(x + A, y + A);
      p.m(x, y + B);
      p.l(x + A, y + B);

      p.m(x + S, y + A);
      p.l(x + B, y + A);
      p.m(x + S, y + B);
      p.l(x + B, y + B);
    }

const ch =
    (x, y) => {
      p.m(x, y + B);
      p.l(x + S, y + B);
      p.m(x, y + A);
      p.l(x + S, y + A);

      p.m(x + A, y + A);
      p.l(x + A, y);
      p.m(x + A, y + B);
      p.l(x + A, y + S);

      p.m(x + B, y + A);
      p.l(x + B, y);
      p.m(x + B, y + B);
      p.l(x + B, y + S);
    }

const drawShape = () => {
  let c = document.getElementById('maze');

  c.setAttribute('width', W * S + S);
  c.setAttribute('height', H * S + S);

  document.getElementById('inner').setAttribute(
      'style', 'width:' + W * S + 'px');

  const I = x_s.length;
  const J = y_s.length;
  ${grid};
  for (var j = 0; j < J; j++) {
    for (var i = 0; i < I; i++) {
      if ((i != 0 || j != J - 1) && (i != I - 1 || j != 0)) {
        grid[j][i](x_s[i], y_s[j]);
      }
    }
  }

  p.dot(x_s[0], y_s[y_s.length - 1]);
  p.dot(x_s[x_s.length - 1], y_s[0]);

  c.innerHTML = p.path();
}