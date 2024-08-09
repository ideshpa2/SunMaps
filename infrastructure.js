const residential = [
    "SF Residential",
    "MF Residential",
    "PUD"
]

const means = {
  "LCZ F (Bare Soil or Sand)": 67.58701116874026,
  "LCZ 10 (Heavy Industry)": 66.60888252148997,
  "LCZ 6 (Open Low Rise)": 65.57173256792201,
  "LCZ 8 (Large Low-rise)": 66.12964671567606,
  "LCZ B (Scattered Trees)": 65.69098712446352,
  "LCZ D (Low Plants)": 67.31403522628544,
  "LCZ 9 (Sparsely Built)": 66.57736223729935,
  "LCZ E (Bare rock or paved)": 67.5252585521082,
  "LCZ 5 (Open Midrise)": 64.99131137603557,
  "LCZ C (Bush, Scrub)": 67.68946705832984,
  "LCZ G (Water)": 66.87418936446174,
  "LCZ 7 (Lightweight Low-rise)": 66.21371769383698,
  "LCZ 4 (Open High-rise)": 66.15862068965517,
  "LCZ A (Dense Trees)": 64.49685534591195
};

//export let tempreduction = 0;

//tree canopy infrastructure
export function treecanopy(lcz, mrt, zoning) {
  let tempreduction = 0;
  let solution = "- No tree canopy <br>";
    // trees work best in low rise, low density neighborhoods
    const bestLczs = [
        "LCZ 6 (Open Low Rise)",
        "LCZ 7 (Lightweight Low-rise)", 
        "LCZ 8 (Large Low-rise)",
        "LCZ 9 (Sparsely Built)" 
    ];

    let treeType = "";
    if (bestLczs.includes(lcz)) {
        if (mrt > means[lcz]) {
            treeType = "non-native deciduous and evergreen trees";
            tempreduction  += 13;
        } else if (mrt === means[lcz]) {
            treeType = "Native trees";
            tempreduction += 8.8;
        } else {
            treeType = "Phoenix Palm trees";
            tempreduction += 5.6;
        }
    

    let percentage = 0;
    if (zoning == "Commercial") {
        percentage = 15;
    } else if (zoning == "Industrial") {
        percentage = 10;
    } else if (residential.includes(zoning)) {
        percentage = 25;
    }

    solution = `- A ${percentage}% increase in tree canopy cover with ${treeType}
            has a projected mean radiant temperature of ${tempreduction} °C. <br>`;
  }
    return solution;
}



//water mister infrastructure
export function watermister(lcz, mrt, zoning) {
  let tempreduction = 0;
  let solution = "";
    const bestLczs = [
        "LCZ 4 (Open High-rise)",
        "LCZ 5 (Open Midrise)", 
        "LCZ 7 (Lightweight Low-rise)", 
        "LCZ 8 (Large Low-rise)",
        "LCZ 10 (Heavy Industry)"
    ];
    if (bestLczs.includes(lcz)) {
        if (zoning === 'Commercial' || zoning === 'Industrial') {

          tempreduction += 8.2
            solution = 
            `- Water misters with a projected temperature reduction of ${tempreduction} °C. <br>`;
        }
    }
    return solution;
}



// reflective pavement infrastructure
export function pavement(lcz, mrt, zoning) {
  let tempreduction = 0;
   let solution = "";
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
    if (mrt > means[lcz]) {
        albedo = 0.7;
    } else if (mrt === means[lcz]) {
        albedo = 0.5;
    } else {
        albedo = 0.3;
    }

    if (lowriseLczs.includes(lcz)) {
        tempreduction += 27;
        return `- Reflective pavement with a ${albedo} albedo
        , with a projected temperature reduction of of ${tempreduction} °C. <br>`;
    } else if (highriseLczs.includes(lcz)) {
        tempreduction += 14;
        return `- Reflective pavement with a ${albedo} albedo
        , with a projected temperature reduction of of ${tempreduction} °C. <br>`;
    }
    return "";

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
    
    if (bestLczs.includes(lcz) && residential.includes(lcz)) {
        tempreduction += 0.3;
    }
    
    return `- cool roofs
    would result in a projected temperature reduction of 8.2 °C <br>`;
}


//artificial shade infrastructure

export function shade(lcz, mrt, zoning) {
 let tempreduction = 0;
  if (['LCZ 4 (Open High-rise)', 'LCZ 5 (Open Midrise)'].includes(lcz)) {
      if (mrt > 35) {
        tempreduction += 23.4;
          return 'Breezeway';
      } else {
        tempreduction +=15.5;
          return 'Tunnel';
  }
 } else if (['LCZ 6 (Open Low Rise)', 'LCZ 7 (Lightweight Low-rise)', 'LCZ 8 (Large Low-rise)'].includes(lcz)) {
      if (mrt > 30) {
        tempreduction += 15.5;
          return 'Overhang with a temperature reduction in ' + tempreduction + '°C <br>';
      } else {
        tempreduction += 15.5;
          return 'Arcade with a temperature reduction in ' + tempreduction + '°C <br>';
  }
 } else if (['LCZ 9 (Sparsely Built)', 'LCZ 10 (Heavy Industry)'].includes(lcz)) {
      if (zoning == 'Industrial') {
        tempreduction+= 6.9;
          return 'PVC_Umbrella with a temperature reduction in ' + tempreduction + '°C <br>';
      } else {
        tempreduction += 15.5;
          return 'Overhang with a temperature reduction in ' + tempreduction + '°C <br>';
  }
 } else if (['LCZ A (Dense Trees)', 'LCZ B (Scattered Trees)'].includes(lcz)) {
      if (residential.includes(zoning)) {
        tempreduction += 6.9;
          return 'Cloth_Umbrella with a temperature reduction in ' + tempreduction + '°C <br>';
      } else {
        tempreduction += 15.5;
          return 'Tunnel with a temperature reduction in ' + tempreduction + '°C <br>';
  } 
}else if (['LCZ C (Bush, Scrub)', 'LCZ D (Low Plants)'].includes(lcz)) {
  tempreduction += 15.5;
      return 'Tunnel with a temperature reduction in ' + tempreduction + '°C <br>';
  } else if (['LCZ E (Bare rock or paved)', 'LCZ F (Bare Soil or Sand)'].includes(lcz)) {
      if (zoning == 'Commercial') {
        tempreduction += 15.5;
          return 'Arcade with a temperature reduction in ' + tempreduction + '°C <br>';
      } else {
        tempreduction += 15.5;
          return 'Tunnel with a temperature reduction in ' + tempreduction + '°C <br>';
  }
 } else if (lcz == 'LCZ G (Water)') {
  tempreduction += 6.9;
      return 'Cloth Umbrella with a temperature reduction in ' + tempreduction + '°C <br>';
  } else {
      return 'no shade';
      }
}
/*export 
function shade(lcz, mrt) {
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
  }*/