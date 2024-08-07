const residential = [
    "SF Residential",
    "MF Residential",
    "PUD"
]
//tree canopy infrastructure
export function treecanopy(lcz, mrt, zoning) {
    // trees work best in low rise, low density neighborhoods
    let projectedMrt = mrt;
    const bestLczs = [
        "LCZ 6 (Open Low Rise)",
        "LCZ 7 (Lightweight Low-rise)", 
        "LCZ 8 (Large Low-rise)",
        "LCZ 9 (Sparsely Built)" 
    ];

    let treeType = "";
    if (bestLczs.includes(lcz)) {
        if (mrt > medians[lcz]) {
            treeType = "Non-native deciduous and evergreen trees";
            projectedMrt -= 13;
        } else if (mrt === medians[lcz]) {
            treeType = "Native trees";
            projectedMrt -= 8.8;
        } else {
            treeType = "Phoenix Palm trees";
            projectedMrt -= 5.6;
        }
    }

    let percentage = 0;
    if (zoning == "Commercial") {
        percentage = 15;
    } else if (zoning == "Industrial") {
        percentage = 10;
    } else if (residential.includes(zoning)) {
        percentage = 25;
    }

    let solution = `For LCZ '${lcz}', MRT ${mrt}, and zoning '${zoning}',
            we recommend a ${percentage}% increase in tree canopy cover with ${treeType},
            with a projected mean radiant temperature of ${projectedMrt} °C.`;
    return solution;
}



//water mister infrastructure
export function watermister(lcz, mrt, zoning) {
    const bestLczs = [
        "LCZ 4 (Open High-rise)",
        "LCZ 5 (Open Midrise)", 
        "LCZ 7 (Lightweight Low-rise)", 
        "LCZ 8 (Large Low-rise)",
        "LCZ 10 (Heavy Industry)"
    ];
    
    let solution;
    if (bestLczs.includes(lcz)) {
        if (zoning === 'commercial' || zoning === 'industrial') {
            solution = `For LCZ '${lcz}', MRT ${mrt}, and zoning '${zoning}',
            recommended water misters would result in a projected mean radiant temperature of ${mrt - 8.2} °C`;
        }
    }
    return solution;
}



// reflective pavement infrastructure
export function pavement(lcz, mrt, zoning) {
    const lowriseLczs = [
        "LCZ 9 (Sparsely Built)", 
        "LCZ D (Low Plants)",   
        "LCZ E (Bare rock or paved)"
    ];
    const highriseLczs = [
        "LCZ 5 (Open Midrise)", 
        "LCZ 6 (Open Low Rise)",
        "LCZ 8 (Large Low-rise)",
        "LCZ 10 (Heavy Industry)"
    ];

    let albedo;
    if (mrt > medians[lcz]) {
        albedo = 0.7;
    } else if (mrt === medians[lcz]) {
        albedo = 0.5;
    } else {
        albedo = 0.3;
    }

    let projectedMrt;
    if (lowriseLczs.includes(lcz)) {
        projectedMrt = mrt - 27;
    } else if (highriseLczs.includes(lcz)) {
        projectedMrt = mrt - 14;
    }

    return `For LCZ '${lcz}', MRT ${mrt}, and zoning '${zoning}',
            we recommend that reflective pavement of a ${albedo} albedo 
            would result in a projected mean radiant temperature of ${projectedMrt} °C`;
}


// cool roof infrastructure
export function coolroof(lcz, mrt, zoning) {
    const bestLczs = [
        "LCZ 4 (Open High-rise)",
        "LCZ 5 (Open Midrise)", 
        "LCZ 7 (Lightweight Low-rise)", 
        "LCZ 8 (Large Low-rise)",
        "LCZ 10 (Heavy Industry)",
        "LCZ B (Scattered Trees)",
        "LCZ D (Low Plants)" 
    ];
    
    if (bestLczs.includes(lcz) && zoning === "residential") {
        projectedMrt = mrt - 0.3;
    }
    
    return `For LCZ '${lcz}', MRT ${mrt}, and zoning '${zoning}',
            recommended cool roofs would result in a projected mean radiant temperature of ${mrt - 8.2} °C`;
}



//artificial shade infrastructure
export function shade(lcz, mrt) {
    console.log("Determining shade for LCZ and MRT:", lcz, mrt);
    if (
      lcz === "LCZ 4 (Open High-rise)" ||
      lcz === "LCZ 5 (Open Midrise)"
    ) {
      if (mrt > 35) {
        return ["Breezeway", 23.4];
      } else {
        return ["Tunnel", 15.5];
      }
    } else if (
      lcz === "LCZ 6 (Open Low Rise)" ||
      lcz === "LCZ 7 (Lightweight Low-rise)" ||
      lcz === "LCZ 8 (Large Low-rise)"
    ) {
      if (mrt > 30) {
        return ["Overhang", 15.5];
      } else {
        return ["Arcade", 15.5];
      }
    } else if (
      lcz === "LCZ 9 (Sparsely Built)" ||
      lcz === "LCZ 10 (Heavy Industry)"
    ) {
      return ["Overhang", 15.5];
    } else if (
      lcz === "LCZ A (Dense Trees)" ||
      lcz === "LCZ B (Scattered Trees)"
    ) {
      return ["Cloth_Umbrella", 6.9];
    } else if (
      lcz === "LCZ C (Bush, Scrub)" ||
      lcz === "LCZ D (Low Plants)"
    ) {
      return ["Tunnel", 15.5];
    } else if (
      lcz === "LCZ E (Bare rock or paved)" ||
      lcz === "LCZ F (Bare Soil or Sand)"
    ) {
      return ["Arcade", 15.5];
    } else if (lcz === "LCZ G (Water)") {
      return ["Cloth_Umbrella", 6.9];
    } else {
      return ["No shade needed", 0.0];
    }
  }