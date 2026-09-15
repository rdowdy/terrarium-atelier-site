// Pure math for a Risset rhythm: N layers of clicks, each layer's rate
// climbing (or falling) by octaves forever, wrapped into an N-octave band,
// under a fixed loudness envelope that is a function of absolute rate
// alone (never of which layer it is).
//
// Every function here takes "shift" directly — the total number of
// octaves the whole comb has drifted since some reference point — rather
// than a time and a speed. That keeps the math indifferent to how shift
// was accumulated: at a constant rate, reversed mid-stream, paused,
// whatever the instrument does with real time is the caller's problem,
// not this file's. This file can be loaded unmodified by the browser and
// by Node for an independent cross-check (see verify.py, which
// reimplements this math from scratch in a different language and diffs
// the results).
(function (root) {
  "use strict";

  // Wrap any real number into [0, N).
  function wrap(x, N) {
    var w = x % N;
    if (w < 0) w += N;
    return w;
  }

  // Layer i's position within the N-octave band, given the comb's total
  // accumulated shift.
  function position(shift, i, N) {
    return wrap(shift + i, N);
  }

  // Instantaneous click rate (Hz) for layer i.
  function rateForLayer(shift, i, N, baseRate) {
    return baseRate * Math.pow(2, position(shift, i, N));
  }

  // The fixed envelope: 0 at both edges of the N-octave band, 1 at the
  // center. A raised-cosine (sin^2) window in log2(rate) space, not a
  // Gaussian: it reaches exact zero (in real-number math; see verify.py
  // for the floating-point caveat) at w=0 and w=N, not an asymptotic
  // near-zero, so the wraparound crosses a mathematically silent point,
  // not a merely very quiet one.
  function envelope(w, N) {
    var s = Math.sin((Math.PI * w) / N);
    return s * s;
  }

  function gainForLayer(shift, i, N) {
    return envelope(position(shift, i, N), N);
  }

  // Sum of all N layers' gains at a given shift. Claimed to be exactly
  // N/2 for every shift, by the identity
  //   sum_{i=0}^{N-1} sin^2(pi*(x+i)/N) = N/2
  // which holds for any real x because sum_{i=0}^{N-1} exp(2*pi*i*i_/N)
  // = 0 for any integer N >= 2 (the Nth roots of unity sum to zero).
  function totalGain(shift, N) {
    var s = 0;
    for (var i = 0; i < N; i++) {
      s += gainForLayer(shift, i, N);
    }
    return s;
  }

  var api = {
    wrap: wrap,
    position: position,
    rateForLayer: rateForLayer,
    envelope: envelope,
    gainForLayer: gainForLayer,
    totalGain: totalGain,
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    root.RissetModel = api;
  }
})(typeof window !== "undefined" ? window : this);
