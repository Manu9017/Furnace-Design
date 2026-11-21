"""Material and finish schedule for parts whose builder does not set one.

Applied after the model is built (only where `material` is empty), so the STEP tree, BOM, drawings and viewer all
carry a material for every physical part. Grades follow Indian standards where SHIVAS buys locally. Where a grade is
an engineering choice rather than a SHIVAS document value it is marked "(A)" and listed as an assumption.
"""

PAINT_HOT = "blast Sa 2½; HR silicone aluminium 2 × 25 µm (to 400 °C)"
PAINT_STD = "blast Sa 2½; zinc phosphate epoxy 75 µm + PU 50 µm"

MATERIAL = {
    # civil
    "CIV-02": "Dense low-cement castable 1,500 °C, 75 mm on SS 304 V-anchors; RCC M30 thickening",
    "CIV-04": "RCC M25, Fe 500D, T12 @ 150 both ways, 40 cover; integral crystalline waterproofing",
    "CIV-05": "Serrated electro-forged grating 40 × 5 @ 30 × 100, HDG to IS 4759",
    "CIV-12": "Serrated electro-forged grating 40 × 5 @ 30 × 100, HDG to IS 4759",
    "CIV-20": "RCC M25, Fe 500D, 250 walls and slab, T12 @ 150 each face; waterproofed",
    "CIV-21a": "IS 3502 chequered plate 8 mm, HDG; SS 304 hinges",
    "HRL-07a": "RCC M25 pedestals, 4 × M24 anchor bolts per pedestal, 25 mm non-shrink grout",
    "STK-02": "RCC M25 base 1,200 × 1,200 × 850; base plate IS 2062 E250 20 mm, 8 × M24 foundation bolts",
    # furnace and casing
    "STR-02": "IS 2062 E250 6 mm, " + PAINT_HOT,
    "STR-11": "IS 3502 chequered plate 6 mm, bolted M12 8.8 to the cap beam; " + PAINT_HOT,
    "KET-02": "Kettle-grade low-Si killed plate, as the kettle shell",
    "PRC-01": "Special high grade zinc ≥ 99.995 % (IS 209), Al 0.005 %",
    "SUP-01": "Moulded graphite strip, density 1.75 g/cm³, 500 segments",
    "TOP-01": "IS 2062 E250 12 mm, continuously welded to the kettle (A)",
    "TOP-02": "HD ceramic-fibre board ~300 kg/m³, 1260 grade (A-04)",
    "TOP-03": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "TOP-04": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "TOP-05": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "TOP-06": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "TOP-08": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "LIN-02": "Microporous board 320 kg/m³, film wrapped",
    "LIN-03": "Calcium silicate board 245 kg/m³, 1,000 °C",
    "LIN-05": "Dense LC castable 1,600 °C, 2,450 kg/m³, SS 310 V-anchors Ø6",
    "LIN-10": "Calcium silicate board 245 kg/m³, 1,000 °C",
    "LIN-11": "Microporous board 320 kg/m³",
    "LIN-12": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "LIN-13": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "LIN-14": "Ceramic-fibre blanket 64 kg/m³, 1260 grade",
    "LIN-15": "HD ceramic-fibre board ~300 kg/m³, laid loose, edges trapped by the wall modules",
    "LIN-16": "Ceramic-fibre board 260 kg/m³, 25 mm",
    "BUR-01": "Bloom HV-400 (vendor item): cast body, SS 310 nozzle",
    "BUR-02": "Bloom HV-400 (vendor item): cast body, SS 310 nozzle",
    "BUR-11": "IS 2062 E250 12 mm plate; M16 8.8 studs; ceramic rope gasket",
    "BUR-12": "IS 2062 E250 12 mm plate; M16 8.8 studs; ceramic rope gasket",
    "INS-01": "Type K duplex in Ti Gr.2 tube (zinc resistant); SS 316 flexible conduit; IP65 Al junction box",
    "INS-02": "Type N, Inconel 600 MI Ø8; SS 316 compression gland",
    # gas, air, burner trains
    "GAS-01": "IS 2062 E250 skid frame ISMC 100, " + PAINT_STD + ", yellow RAL 1003 piping bands",
    "GAS-02": "Seamless ASTM A106 Gr.B Sch 40, butt-welded, RT 10 %; flanges ASME B16.5 Cl.150; " + PAINT_STD + " RAL 1003",
    "GAS-05": "RCC M20 sleepers with 150 × 75 × 6 SS 304 slide pads",
    "GAS-06": "ASTM A106 Gr.B Sch 40, rain cap and flame arrester at +12.5",
    "NG-50-101": "ASTM A106 Gr.B Sch 40 DN50, butt-welded, RT 10 %, hydrotest 1.5 × MOP; RAL 1003",
    "NG-15-112": "ASTM A106 Gr.B Sch 80 DN15, socket-welded; RAL 1003",
    "NG-15-122": "ASTM A106 Gr.B Sch 80 DN15, socket-welded; RAL 1003",
    "NG-40-111": "ASTM A106 Gr.B Sch 40 DN40, butt-welded; RAL 1003",
    "NG-40-121": "ASTM A106 Gr.B Sch 40 DN40, butt-welded; RAL 1003",
    "NG-50-113": "ASTM A106 Gr.B Sch 40 DN50 with forged tee ASME B16.9; RAL 1003",
    "NG-50-123": "ASTM A106 Gr.B Sch 40 DN50 with forged tee ASME B16.9; RAL 1003",
    "IMP-1": "Copper tube ¼\" annealed, brass compression fittings",
    "IMP-2": "Copper tube ¼\" annealed, brass compression fittings",
    "AIR-01": "RCC M20 plinth; ISMC 100 frame; neoprene AVMs 50 Shore A",
    "CA-200-101": "ERW MS pipe 7\" × 3.2 (IS 3589), flanged; " + PAINT_STD + " RAL 5012",
    "CA-300-101": "MS sheet 2 mm, flanged L 40 × 40 × 5; " + PAINT_STD + " RAL 5012",
    "CA-150-103": "MS sheet 2 mm, seam-welded; " + PAINT_STD + " RAL 5012",
    "CA-100-11": "ERW MS pipe 4\" × 3.2 (IS 1239); " + PAINT_STD + " RAL 5012",
    "CA-100-12": "ERW MS pipe 4\" × 3.2 (IS 1239); " + PAINT_STD + " RAL 5012",
    "CA-15-101": "GI pipe ½\" medium (IS 1239) to the C9 cocks; SS braided flexibles",
    "VEN-PF-N": "Centrifugal fan, MS casing, spark-resistant aluminium impeller (LPG pit), 3 HP flameproof motor (A)",
    "VEN-PF-S": "Centrifugal fan, MS casing, spark-resistant aluminium impeller (LPG pit), 3 HP flameproof motor (A)",
    "VEN-PF-Nd": "GI sheet 1.0 mm spiral duct Ø280",
    "VEN-PF-Sd": "GI sheet 1.0 mm spiral duct Ø280",
    "PIT-N1": "MS pipe 32 NB medium posts and rails, toe board 100 × 6; " + PAINT_STD + " RAL 1003",
    "PIT-S1": "MS pipe 32 NB medium posts and rails, toe board 100 × 6; " + PAINT_STD + " RAL 1003",
    "PIT-N2": "HDG flat 50 × 20 stringers, Ø20 rungs",
    "PIT-S2": "HDG flat 50 × 20 stringers, Ø20 rungs",
    # flue
    "FLU-07": "Type K MI Inconel 600 in SS 310 thermowell 1\"",
    "FLU-08": "SS 316 ¼\" tube and fittings; transmitter wetted parts SS 316",
    # loop
    "HRL-05": "IS 2062 E250 6 mm, " + PAINT_HOT + "; 50 mm mineral wool + 0.8 mm Al cladding outside",
    "HRL-05a": "IS 2062 E250 6 mm, " + PAINT_HOT,
    "HRL-06": "GI 1.6 mm blades with 10 mm hem, SS 304 spindles, nylon bushes",
    "HRL-06a": "Belimo LM230A-S (vendor item)",
    "HRL-07": "AEP-ZA-9.0 (vendor item): MS casing 5 mm, backward-curved impeller, dynamically balanced G2.5",
    "HRL-07b": "IS 2062 E250 ISMC 200, " + PAINT_STD,
    "HRL-07c": "IS 2062 E250 3 mm, " + PAINT_HOT,
    "HRL-07d": "Silicone-coated glass fabric, 200 °C, MS flanges",
    "HRL-07e": "IS 2062 E250 4 mm",
    "HRL-07f": "EN19 shaft Ø100; SN-series plummer blocks with spherical roller bearings, grease lubricated",
    "HRL-07g": "Expanded metal 25 × 10 on L 25 × 25 frame, RAL 1003",
    "HRL-07h": "TEFC IE3 22 kW 4-pole, IP55, Class F, on VFD",
    "HRL-12": "IS 2062 E250 3 mm, spiral-welded; 50 mm mineral wool 100 kg/m³ + 0.8 mm Al cladding",
    "HRL-12a": "IS 2062 E250 3 mm",
    "HRL-12b": "IS 2062 E250 ISMC 150, PTFE/SS slide saddles",
    "HRL-09": "IS 2062 E250 4 mm, " + PAINT_HOT,
    "HRL-09a": "Butterfly Ø400, MS body, SS 304 shaft, locking quadrant",
    "HRL-10": "Finned-tube coil SS 304 tubes / Al fins in MS casing (A)",
    "HRL-11": "IS 2062 E250 ISMB 100, " + PAINT_STD,
    "STK-01": "IS 2062 E250 6 mm, " + PAINT_HOT + "; Cu lightning conductor 25 × 3",
    "STK-03": "HDG platform grating, MS handrails, ladder with cage above 2.5 m",
    # dryer
    "DRY-02r": "BK50 helical-bevel gearmotor 1.1 kW with brake; pinion EN19 hardened; shaft EN8",
    "DRY-03r": "BK50 helical-bevel gearmotor 1.1 kW with brake; pinion EN19 hardened; shaft EN8",
    "DRY-04p": "GI 2 mm perforated",
    "DRY-05p": "GI 2 mm perforated",
    "DRY-06": "GI 2 mm with silicone flexible seal",
    "DRY-07": "Roller chain ISO 16B-1 (25.4 pitch), case-hardened pins, high-temperature grease",
    "DRY-09": "IS 2062 E250 angles with UHMW-PE wear strips (to 120 °C)",
    "DRY-13": "IS 2062 E250 10 mm, hardened wear pads",
    "DRY-14": "Helical-bevel gearmotors 3.7 kW with brake and encoder, IP55, on VFDs (A-17)",
    "DRY-15": "Duplex Pt100 Class A in SS 316 Ø8 sheath",
    "DRY-16": "Al die-cast pedestal station, IP65",
    # enclosure
    "ZEN-05a": "Heavy-duty limit switches IP67; nylon drag chain",
    "ZEN-05c": "IS 2062 E250 carriage plate 20 mm; worm slew drive (vendor item, A-16); 0.75 kW brake motor with encoder",
    "ZEN-07aG": "Glass-ceramic 5 mm (700 °C) in SS 304 frames",
    "ZEN-07aI": "Ceramic-fibre blanket 128 kg/m³ 1260 grade + microporous 25 mm",
    "ZEN-07aS": "Silicone-glass fibre rope seals; brush strips with SS 304 backing and aramid bristles",
    "ZEN-07bG": "Toughened glass 8 mm in removable MS frames with silicone gaskets",
    "ZEN-08a": "Electric chain hoists 2 t, 4 m/min, IP55, Class F, with overload and slack-chain switches",
    "ZEN-08b": "Electric chain hoists 1 t, 8 m/min, IP55, Class F",
    "ZEN-08aC": "Grade 80 load chain, zinc-flake coated",
    "ZEN-08bC": "Grade 80 load chain, zinc-flake coated",
    "ZEN-09aM": "Helical-bevel gearmotor 0.37 kW with brake, IP55",
    "ZEN-09bM": "Helical-bevel gearmotor 0.37 kW with brake, IP55",
    "ZEN-10": "LED floodlight 200 W, die-cast Al, IP66, 80 °C ambient",
    "ZEN-10a": "Toughened glass lens",
    "ZEN-11a": "IS 2062 E250 3 mm doors with silicone gaskets, M10 SS 304 bolts",
    "ZEN-12": "IS 2062 E250 3 mm, inside zinc-rich epoxy",
    "ZEN-13": "IS 2062 E250 4 mm, inside zinc-rich epoxy; long-radius bends",
    "ZEN-13a": "IS 2062 E250 ISHB 150, " + PAINT_STD,
    "ZEN-13b": "Butterfly Ø700, MS body, SS 304 shaft, electric actuator IP65",
    "ZEN-14": "Pt100 SS 316; ΔP transmitter ±100 Pa; LCS in powder-coated MS IP55 enclosure",
    # loads, references
    "JIG-01": "IS 2062 E250 ISMB 200 jig beams, hooks and wire (sample loads)",
    "REF-01": "—",
}


def apply(R):
    n = 0
    for p in R.parts:
        if p.layer == "flow" or p.material:
            continue
        m = MATERIAL.get(p.tag)
        if m:
            p.material = m
            n += 1
    return n
