"""Flue duct, heat-recovery loop (trenches, mixing box, recirculation blower), 4-position dryer, bleed & stack,
zinc fume enclosure, sample loads, scale figures."""
from __future__ import annotations

import math

from ..basis import B, G
from .lib import box, compound, cyl, duct, frame, ibeam, merge, pipe, prism_x, prism_y, quarter_ring, rrect, sph, tube

FLOWCOL = {"HRL-02a": "retn", "HRL-02b": "retn", "HRL-03": "suct", "HRL-04": "suct", "HRL-08": "supp"}
FLOWNAME = {"HRL-02a": "Return trench 900 × 1,000 (from the dryer)", "HRL-02b": "Return trench 900 × 1,000 (to the junction)",
            "HRL-03": "Three-way junction 1,000 × 1,000 (return + flue → suction)", "HRL-04": "Suction trench 1,000 × 1,000",
            "HRL-08": "Discharge trench 1,100 × 1,000 (blower at the SW corner → supply box)"}
FLOWSPEC = {"HRL-02a": "28,614 Nm³/h at 100 °C = 10.86 m³/s, 12.1 m/s", "HRL-02b": "28,614 Nm³/h at 100 °C, 12.1 m/s",
            "HRL-03": "10.86 + 1.41 = 12.27 m³/s, radiused merge", "HRL-04": "12.27 m³/s at ≈124–130 °C, 12.3 m/s",
            "HRL-08": "48,000 m³/h at 120 °C = 13.33 m³/s from the blower, 11.44 m³/s after the bleed; 12.1 m/s"}


def _flue_solid(a, b, ext=0.0):
    """Lined flue duct envelope with half-width a, half-height b along the D-26 route: stub, R700 bend, west run."""
    g = G
    xc, zc = g.flue_xc, g.flue_zc
    cx, cy = g.flue_bend_c
    Rc, ys, yr, xe = g.flue_R, g.flue_ys, g.flue_run_y, g.flue_end_x
    stub = box(xc - a, xc + a, ys, g.flue_y_ej[1] + ext, zc - b, zc + b)
    bend = quarter_ring(cx, cy, Rc - a, Rc + a, zc - b, zc + b, (1, -1))
    run = box(xe - ext, cx, yr - a, yr + a, zc - b, zc + b)
    return stub.union(bend).union(run)


def build_flue(R):
    """Lined flue duct (D-10 build-up, D-26 route): leaves the south end wall at the SW corner just above the hearth,
    passes an expansion joint, turns west on an R700 bend in the bottom-left corner of the south burner pit and runs
    through the pit's west wall into the junction. Every change of direction is radiused; nothing is mitred."""
    g = G
    xc, zc = g.flue_xc, g.flue_zc
    W, H, tl, ts = 700, 400, 150, 6
    a_o, b_o = W / 2 + tl + ts, H / 2 + tl + ts            # 506 / 356
    a_l, b_l = W / 2 + tl, H / 2 + tl                      # 500 / 350
    a_g, b_g = W / 2, H / 2                                # 350 / 200
    shell = _flue_solid(a_o, b_o).cut(_flue_solid(a_l, b_l, ext=1))
    lining = _flue_solid(a_l, b_l).cut(_flue_solid(a_g, b_g, ext=1))
    y0, y1 = g.flue_y_ej
    fr = lambda y: box(xc - 560, xc + 560, y - 20, y, zc - 410, zc + 410).cut(box(xc - a_l, xc + a_l, y - 21, y + 1, zc - b_l, zc + b_l))
    flanges = compound(fr(-g.cYo - 12), fr(y1 + 20))
    bolts = compound(*[cyl((x, y - 20, z), (x, y - 50, z), 8) for y in (-g.cYo - 12,) for x in (xc - 520, xc, xc + 520) for z in (zc - 380, zc + 380)],
                     *[cyl((x, y + 20, z), (x, y + 50, z), 8) for y in (y1,) for x in (xc - 520, xc, xc + 520) for z in (zc - 380, zc + 380)])
    ej = box(xc - a_o - 30, xc + a_o + 30, y1 + 20, y0, zc - b_o - 30, zc + b_o + 30).cut(box(xc - a_g, xc + a_g, y1, y0, zc - b_g, zc + b_g))
    ej = ej.cut(compound(*[box(xc - a_o - 31, xc + a_o + 31, y - 6, y + 6, zc + b_o + 10, zc + b_o + 31) for y in (y0 - 70, y1 + 70)]))
    ys = g.flue_ys
    R.add("FLU-01 Lined flue duct", merge(shell, flanges, bolts), "flue", "fluesteel", tag="FLU-01", title="Lined flue duct, south end → R700 bend → junction (D-26)",
          spec="700 × 400 clear (0.28 m², ≈5.4 m/s at 800 °C); 6 mm shell with 75 × 75 × 6 angle stiffening rings @ 600; flange frames 1,120 × 820 × 20 "
               "with M16 bolts @ 150 and ceramic rope gaskets; horizontal 90° bend on a 700 centreline radius (inner 350, outer 1,050 on the gas side) in the "
               "SW corner of the south burner pit; run west through the pit wall sleeve into the junction; slopes 0; total ≈2.1 m",
          material="IS 2062 E250 shell; bolts 8.8 HDG; outside HR silicone aluminium", src="D-10 (construction) · D-26 (route, owner instruction 21 Nov)", status="D",
          note="Skin ≈80 °C: guarded where people can reach it (FLU-05).")
    R.add("FLU-02 Flue duct lining", lining, "flue", "module", tag="FLU-02", title="Flue duct lining 150 mm",
          spec="100 mm folded module 128 kg/m³ 1430 grade (hot face) + 50 mm microporous; modules on SS 310 M8 studs @ 300 × 300 with SS 310 speed washers; "
               "bend lined with segmented modules cut on the radius, joints staggered", material="Ceramic fibre 1430 grade; microporous 320 kg/m³; studs SS 310",
          src="D-10 · C-04", status="D")
    R.add("FLU-04 Fabric expansion joint", ej, "flue", "rubber", tag="FLU-04", title="Fabric expansion joint at the casing",
          spec="200 face-to-face, PTFE/glass-fibre multilayer with 50 mm fibre pillow, rated 600 °C gas side; takes the casing's growth and ±15 mm misalignment",
          material="PTFE-coated glass fabric + SS 304 flanges", src="this design", status="D")
    # supports: stools on the pit floor and in the link trench, sliding plates
    cx, cy = g.flue_bend_c
    pts = [(cx + g.flue_R * math.cos(math.radians(t)), cy + g.flue_R * math.sin(math.radians(t))) for t in (-22, -68)] + [(-1850, g.flue_run_y)]
    st = []
    for (x, y) in pts:
        fl = g.bpit_floor if x > -1500 else g.trench_floor_k["FLUE"]
        st += [box(x - 150, x + 150, y - 150, y + 150, fl, zc - b_o - 30), box(x - 260, x + 260, y - 260, y + 260, zc - b_o - 30, zc - b_o - 6),
               box(x - 300, x + 300, y - 300, y + 300, zc - b_o - 6, zc - b_o)]
    R.add("FLU-03 Duct stools", compound(*st), "flue", "steel2", tag="FLU-03", title="Flue duct stools with PTFE sliding plates",
          spec="Fabricated from ISMC 150 + 20 mm base plate, 2 × M16 anchors; 3 mm PTFE on SS slide plates; the junction end is the fixed point",
          material="IS 2062 E250; PTFE/SS 304 slide", src="this design", status="D", qty=str(len(pts)))
    guard = _flue_solid(a_o + 75, b_o + 75).cut(_flue_solid(a_o + 72, b_o + 72, ext=1)).intersect(box(-1499, 0, -5900, -g.cYo - 230, zc - b_o + 40, zc + b_o + 80))
    R.add("FLU-05 Personnel guard", guard, "flue", "grating", tag="FLU-05", title="Expanded-metal personnel guard over the flue duct (south pit)",
          spec="Expanded metal 50 × 25 × 3, 75 off the shell, on bolted brackets; removable in four sections", material="GI expanded metal", src="this design", status="D", alpha=0.45)
    t = math.radians(-45)
    rr = g.flue_R + a_o + 21
    door = box(-20, 25, -260, 260, -170, 170).union(box(25, 45, -40, 40, -20, 20)).rotate((0, 0, 0), (0, 0, 1), -45).translate((cx + rr * math.cos(t), cy + rr * math.sin(t), zc))
    R.add("FLU-06 Inspection and cleanout door", door, "flue", "steel", tag="FLU-06", title="Inspection and ash-cleanout door on the bend",
          spec="500 × 300 clear on the outer wall of the bend at 45°, bolted, with a 150 mm fibre plug and rope gasket", material="IS 2062 E250", src="this design", status="D")
    te = merge(cyl((xc - 200, ys + 25, zc + b_o), (xc - 200, ys + 25, zc + b_o + 180), 14), box(xc - 260, xc - 140, ys - 35, ys + 85, zc + b_o + 180, zc + b_o + 280))
    pt = merge(cyl((xc + 200, ys + 25, zc + b_o), (xc + 200, ys + 25, zc + b_o + 120), 10),
               pipe([(xc + 200, ys + 25, zc + b_o + 120), (xc + 200, ys + 25, -500), (-1440, ys + 25, -500), (-1440, -4700, -500)], 6),
               box(-1495, -1385, -4800, -4600, -620, -380))
    R.add("FLU-07 Flue thermocouple TE-301", te, "instr", "galv", tag="FLU-07", title="Flue gas thermocouple TE-301",
          spec="Type K, Inconel 600 MI Ø8, U = 250, in a 1\" SS 310 thermowell on the stub; to the PLC (O-02 commissioning data)", src="this design", status="D")
    R.add("FLU-08 Furnace pressure tap PT-301", pt, "instr", "panel", tag="FLU-08", title="Furnace pressure transmitter PT-301",
          spec="±50 Pa low-range ΔP transmitter on the pit wall, ¼\" SS impulse from the stub, condensate pot; set point −2 to −5 Pa at the hearth", src="this design", status="D")
    passage = box(*g.flue_pass_X, -g.cYi, -g.lfY, *g.flue_pass_z)
    R.add("FLOW-flue Flue gas", merge(_flue_solid(a_g - 20, b_g - 20), passage), "flue", "flue", tag="FLOW", title="Flue gas 800 °C",
          spec="1,386 Nm³/h at design λ (Rev H 1,296), 1.54 m³/s", src="C-01 · C-07", status="C", alpha=0.45, layer="flow")


def build_trenches(R):
    g = G
    clears = dict(g.trenches)
    clears["FLUE"] = g.flue_trench
    mb = g.mb
    clears["MBPIT"] = (mb[0], mb[1], mb[2], mb[3])
    outer, inner = None, None
    for k, (x0, x1, y0, y1) in clears.items():
        t = 250 if k == "MBPIT" else 200
        zf = g.trench_floor_k.get(k, -1000)
        if k == "FLUE":          # short link between the junction and the south pit wall: side walls and floor only
            o = box(x0, x1, y0 - t, y1 + t, zf - t, 0)
            i = box(x0 - 201, x1 + 1, y0 - 1, y1 + 1, zf, 10)
        else:
            o = box(x0 - t, x1 + t, y0 - t, y1 + t, zf - t, 0)
            i = box(x0 - 1, x1 + 1, y0 - 1, y1 + 1, zf, 10)
        outer = o if outer is None else outer.union(o)
        inner = i if inner is None else inner.union(i)
    rcc = outer.cut(inner)
    # junction sump benching (60°) from the -1.000 trench floors down to the -1.350 sump floor
    jx0, jx1, jy0, jy1 = g.trenches["HRL-03"]
    zj = g.trench_floor_k["HRL-03"]
    bench = merge(prism_x([(jy1, zj), (jy1, -1000), (jy1 - 200, zj)], jx0, jx1), prism_x([(jy0, zj), (jy0, -1000), (jy0 + 200, zj)], jx0, jx1))
    rcc = rcc.union(bench)
    R.add("CIV-10 Loop trenches and mixing-box pit", rcc, "civil", "concrete2", tag="CIV-10", title="Heat-recovery trenches and mixing-box pit (RCC)",
          spec="RCC M25, 200 walls and floor, T12 @ 150, waterproofed (crystalline admixture + external membrane); clear depth 1,000 (Hold H1); "
               "junction sump floor −1.350 with 60° benching (D-26); flue link floor −1.650; mixing-box pit 1,500 × 1,300, floor −1.100, 250 walls",
          material="RCC M25, Fe 500D", src="Rev H · SH-MB-01 Rev A · HDG · D-26", status="O", note="Hold H1: R-02 foundation drawings show −1,400 / −1,000 (O-01).")
    face = box(jx0, jx0 + 75, g.flue_run_y - 380, g.flue_run_y + 380, zj + 75, -300).union(box(jx0, jx1, g.flue_run_y - 380, g.flue_run_y + 380, zj, zj + 75))
    R.add("HRL-03a Junction impingement facing", face, "loop", "castable", tag="HRL-03a", title="Junction refractory facing opposite the flue inlet",
          spec="75 mm dense castable on SS 304 V-anchors, west wall and sump floor where the 800 °C flue gas lands; keeps the RCC under 65 °C",
          material="LC castable 1,500 °C", src="D-26 · C-04", status="D")
    covers = []
    for k, (x0, x1, y0, y1) in g.trenches.items():
        c = box(x0 - 100, x1 + 100, y0 - 100, y1 + 100, -8, 0)
        if k == "HRL-08":
            c = c.cut(cyl((g.bleed[0], g.bleed[1], -20), (g.bleed[0], g.bleed[1], 20), 210))
            c = c.cut(box(g.rb_axis[0] - 101, g.rb_axis[1] + 50, g.rb_axis[2] - 1000, g.rb_axis[2] + 1000, -20, 20))
        if (x1 - x0) > (y1 - y0):
            for x in range(int(x0), int(x1), 1000):
                c = c.cut(box(x - 2, x + 2, y0 - 101, y1 + 101, -9, 1))
        else:
            for y in range(int(y0) + 1000, int(y1), 1000):
                c = c.cut(box(x0 - 101, x1 + 101, y - 2, y + 2, -9, 1))
        covers.append(c)
    R.add("CIV-11 Trench cover plates", compound(*covers), "civil", "deck", tag="CIV-11", title="Trench cover plates",
          spec="8 mm chequered plate in 1 m removable sections on embedded ISA 50 × 50 × 6 nosing with lifting holes; 5 kN/m² pedestrian",
          material="IS 3502 chequered plate, HDG", src="Rev H · HDG", status="C")
    fx0, fx1, fy0, fy1 = g.flue_trench
    R.add("CIV-12 Flue trench grating", box(-1950, fx1, fy0 - 100, fy1 + 100, -40, 0), "civil", "grating", tag="CIV-12", title="Flue link vented grating",
          spec="Serrated grating 40 × 5 @ 30 so the link breathes (D-10); the duct inside is lined", src="D-10 · D-26", status="D")
    for k, (x0, x1, y0, y1) in g.trenches.items():
        R.add(f"FLOW-{k} {FLOWNAME[k]}", box(x0 + 20, x1 - 20, y0 + 20, y1 - 20, -980, -20), "loop", FLOWCOL[k], tag=k, title=FLOWNAME[k],
              spec=FLOWSPEC[k], src="Rev H heat-recovery loop · C-08 · C-09", status="C", alpha=0.35, layer="flow")


def build_mixing_box(R):
    g = G
    x0, x1, y0, y1, zf, zr = g.mb
    t = 6
    steel = box(x0 - t, x1 + t, y0 - t, y1 + t, 0, zr + t).cut(box(x0, x1, y0, y1, -1, zr))
    steel = steel.cut(cyl((x0 - 10, (y0 + y1) / 2, 900), (x0 + 10, (y0 + y1) / 2, 900), 557))
    bands = [frame(x0 - t - 60, x1 + t + 60, y0 - t - 60, y1 + t + 60, x0 - t, x1 + t, y0 - t, y1 + t, z, z + 60) for z in (200, 700, 1200)]
    ring = tube((x0 - 60, (y0 + y1) / 2, 900), (x0 - t, (y0 + y1) / 2, 900), 640, 557)
    R.add("HRL-05 Mixing box S2", merge(steel, compound(*bands), ring), "loop", "steel2", tag="HRL-05", title="Mixing box, configuration S2",
          spec="1,500 × 1,300 × 2,700 internal (1,100 pit + 1,600 steel); floor −1.100, roof +1.600; 5.27 m³; rise 6.84 m/s, 0.40 s; blower cut-out Ø1,114 at +0.900 (west face)",
          src="SH-MB-01 Rev A", status="C", note="Blower cut-out face differs between Rev N and SH-MB-01 (O-09); the model follows SH-MB-01.")
    yc = (y0 + y1) / 2
    vane = quarter_ring(0, 0, 694, 700, x0, x1, (-1, -1))   # built about origin then placed
    vane = cyl((x0, y0 + 700, zf + 700), (x1, y0 + 700, zf + 700), 700).cut(cyl((x0 - 1, y0 + 700, zf + 700), (x1 + 1, y0 + 700, zf + 700), 694))
    vane = vane.intersect(box(x0, x1, y0, y0 + 700, zf, zf + 700))
    R.add("HRL-05a Turning deflector R700", vane, "loop", "galv", tag="HRL-05a", title="Turning deflector R700",
          spec="6 mm plate; cuts the turn loss from K 1.2 to 0.40 (9.2 mmWC)", src="SH-MB-01 Rev A", status="C")
    # fresh-air damper on the far (south) face, sleeve 500 at 30 deg down, damper at the outer end
    sx, sz = (x0 + x1) / 2, 700
    sleeve = box(sx - 175, sx + 175, y0 - 500, y0, sz - 175, sz + 175).rotate((sx, y0, sz), (sx + 1, y0, sz), -30)
    ang = math.radians(30)
    ex, ey, ez = sx, y0 - 500 * math.cos(ang), sz - 500 * math.sin(ang)
    damper = box(ex - 200, ex + 200, ey - 150, ey, ez - 200, ez + 200).rotate((ex, ey, ez), (ex + 1, ey, ez), -30)
    act = box(ex + 200, ex + 330, ey - 120, ey - 20, ez - 60, ez + 60)
    cowl = box(ex - 260, ex + 260, ey - 420, ey - 150, ez + 150, ez + 230).rotate((ex, ey, ez), (ex + 1, ey, ez), -30)
    R.add("HRL-06 Fresh-air make-up damper", merge(sleeve, damper, cowl), "loop", "galv", tag="HRL-06", title="Fresh-air make-up damper STL-MB-DMP-02",
          spec="350 × 350 opposed blade, GI, SS304 spindles, 1.6 mm blades with 10 mm hem; sleeve 500 at 30° below horizontal; cowl + bird mesh; min stop ≈15 % open; 3,433 Nm³/h",
          src="STL-MB-DMP-02 Rev A · Rev H", status="C")
    R.add("HRL-06a Damper actuator", act, "instr", "panel", tag="HRL-06a", title="Belimo LM230A-S actuator", spec="5 N·m on/off, PLC DO → relay", src="STL-MB-DMP-02 Rev A", status="C")
    R.add("FLOW-mix Mixing zone", box(x0 + 30, x1 - 30, y0 + 30, y1 - 30, zf + 30, zr - 30), "loop", "suct", tag="FLOW", title="Mixed gas ≈124 °C",
          spec="flue + return + fresh air (C-08 adiabatic mix 124 °C)", src="C-08", status="C", alpha=0.3, layer="flow")


def build_blower(R):
    """Recirculation blower at the SW corner where the discharge turns north into the dryer (D-22, user instruction).
    Fan axis at +0.90 on the mixing-box cut-out, so the long suction duct runs straight; outlet drops into HRL-08."""
    g = G
    sx0, sx1, yc, zc = g.rb_axis
    r = g.rb_r
    dx0, dx1, _yd, _zd, rd = g.suction                 # Ø1100 duct from the mixing box (dx0) to the reducer (dx1)
    ped = compound(box(-14100, -12150, -8800, -6400, 0, 300), box(-10650, -10050, -8800, -6400, 0, 300))
    frm = compound(*[box(-14000, -10100, y - 50, y + 50, 300, 500) for y in (-8750, -6450)],
                   *[box(x - 50, x + 50, -8800, -6400, 300, 500) for x in (-13950, -12250)], box(-10650, -10550, -8800, -6400, 300, 400))
    lugs = compound(box(sx0 + 60, sx1 - 60, -8750, -8550, 500, zc), box(sx0 + 60, sx1 - 60, -6650, -6450, 500, zc))
    R.add("HRL-07a Blower pedestals", ped, "civil", "concrete2", tag="HRL-07a", title="Recirculation blower pedestals",
          spec="RCC, west and east of the discharge trench at the SW corner", src="D-22", status="D")
    R.add("HRL-07b Blower base frame", merge(frm), "loop", "steel", tag="HRL-07b", title="Blower base frame",
          spec="ISMC 200 frame bridging the trench (east cross member lowered under the straightener spool); scroll on side lugs, outlet drops straight into HRL-08", src="D-22", status="D")
    scroll = cyl((sx0, yc, zc), (sx1, yc, zc), r)
    outlet = box(sx0, sx0 + 675, yc - 950, yc - 50, -400, zc - r + 40)
    R.add("HRL-07 Recirculation blower", merge(scroll, outlet, lugs), "loop", "fan", tag="HRL-07", title="Recirculation blower AEP-ZA-9.0 (SW corner)",
          spec="48,000 m³/h at 120 °C, 72 mmWC, 30 HP; Ø900 inlet facing east on the axis +0.900; 900 × 675 outlet straight down into the 1,100 × 1,000 trench where it turns north to the dryer",
          src="Rev H · user instruction 21 Nov · D-22", status="C", note="Confirm whether 72 mmWC is a 20 °C or 120 °C rating (O-07).")
    clad = 600
    duct = cyl((dx0, yc, zc), (dx1, yc, zc), clad).cut(cyl((dx0 - 1, yc, zc), (dx1 + 1, yc, zc), rd - 3))
    flange = tube((dx0 - 20, yc, zc), (dx0, yc, zc), 640, rd)
    red = __import__("cadquery").Workplane().add(__import__("cadquery").Solid.makeCone(rd + 50, 450 + 50, 400, __import__("cadquery").Vector(dx1, yc, zc),
                                                                                     __import__("cadquery").Vector(-1, 0, 0)))
    spool = tube((dx1 - 400, yc, zc), (sx1 + 150, yc, zc), 456, 450)
    flex = cyl((sx1 + 150, yc, zc), (sx1, yc, zc), 480)
    cross = compound(box(sx1 + 170, sx1 + 730, yc - 445, yc + 445, zc - 2, zc + 2), box(sx1 + 170, sx1 + 730, yc - 2, yc + 2, zc - 445, zc + 445))
    stools = compound(*[merge(box(x - 75, x + 75, yc - 450, yc + 450, 0, zc - clad - 60), box(x - 120, x + 120, yc - 420, yc + 420, zc - clad - 60, zc - clad - 1)) for x in (-9200, -6900, -4600)])
    L = (dx0 - dx1) / 1000
    R.add("HRL-12 Suction duct Ø1100", merge(duct, flange), "loop", "alu", tag="HRL-12", title="Suction duct Ø1100, mixing box → blower",
          spec=f"Ø1100 × 3 mm MS, {L:.2f} m straight at +0.900 from the Ø1,114 cut-out on the mixing-box west face; 50 mm mineral wool + 0.8 mm aluminium cladding (Ø1,200 over cladding); ≈12.9 m/s",
          src="user instruction 21 Nov · D-22 · SH-MB-01 Rev A", status="D", note="Lengthened when the blower moved to the SW corner; Ø1100 keeps the added loss ≈2 mmWC (C-09).")
    R.add("HRL-12a Reducer Ø1100 → Ø900", red, "loop", "galv", tag="HRL-12a", title="Concentric reducer Ø1100 → Ø900", spec="400 long, 3 mm MS", src="D-22", status="D")
    R.add("HRL-07c Straightener spool Ø900", spool, "loop", "galv", tag="HRL-07c", title="Straightener spool Ø900 at the fan inlet",
          spec="600 long; holds the cruciform straightener immediately ahead of the fan eye", src="SH-MB-01 Rev A · D-22", status="D")
    R.add("HRL-07d Inlet flexible connector", flex, "loop", "rubber", tag="HRL-07d", title="Inlet flexible connector", spec="High-temperature fabric, 150 °C", src="this design", status="D")
    R.add("HRL-07e Cruciform straightener", cross, "loop", "steel2", tag="HRL-07e", title="Cruciform straightener",
          spec="2 × 4 mm plates ≈560 long (mandatory per SH-MB-01)", src="SH-MB-01 Rev A", status="C")
    R.add("HRL-12b Duct stools", stools, "loop", "steel2", tag="HRL-12b", title="Suction duct support stools", spec="3 stools with sliding saddles; fixed point at the fan end", src="D-22", status="D")
    shaft = cyl((sx0, yc, zc), (-13050, yc, zc), 50)
    pb = compound(*[box(x - 120, x + 120, yc - 180, yc + 180, 500, zc - 60) for x in (-12350, -12750)])
    guard = box(-13250, -12950, yc - 180, yc + 180, 450, zc + 300)
    motor = cyl((-14000, yc, 760), (-13300, yc, 760), 260)
    mbase = box(-14000, -13300, yc - 260, yc + 260, 500, 520)
    R.add("HRL-07f Fan shaft and bearings", merge(shaft, pb), "loop", "gear", tag="HRL-07f", title="Fan shaft and plummer blocks", spec="Shaft Ø100, 2 × plummer blocks", src="HDG", status="C")
    R.add("HRL-07g Belt guard", guard, "loop", "yellow", tag="HRL-07g", title="Belt guard", spec="Expanded mesh, yellow", src="HDG", status="C")
    R.add("HRL-07h Blower motor 30 HP", merge(motor, mbase), "loop", "motor", tag="HRL-07h", title="Recirculation blower motor 30 HP (22 kW), VFD",
          spec="Cold start ≈16 kW shaft (C-11)", src="Rev H · C-11", status="C")
    R.add("FLOW-suction Suction duct gas", cyl((dx0 - 20, yc, zc), (sx1 + 160, yc, zc), 430), "loop", "suct", tag="FLOW", title="Mixed gas ≈124 °C to the blower",
          spec="12.27 m³/s", src="C-08", status="C", alpha=0.3, layer="flow")


def build_dryer(R):
    g = G
    X0, X1, Y = g.dX0, g.dX1, g.dY
    li, wl = g.d_lin, g.d_wall
    zf = g.d_floor
    rx0, rx1, ry = X0 - li, X1 + li, Y + li                  # RCC inner
    ox0, ox1, oy = rx0 - wl, rx1 + wl, ry + wl              # RCC outer
    rcc = box(ox0, ox1, -oy, oy, zf - li - 250, 0).cut(box(rx0, rx1, -ry, ry, zf - li, 1))
    for xa, xb, w in ((ox0 - 1, X0 + 1, 500), (X1 - 1, ox1 + 1, 450)):
        rcc = rcc.cut(box(xa, xb, -w, w, -1000, -300))
    rcc = rcc.cut(cyl((-5000, ry - 10, -500), (-5000, oy + 10, -500), 70))
    R.add("CIV-20 Dryer pit", rcc, "civil", "rccpit", tag="CIV-20", title="Dryer pit (RCC)",
          spec=f"RCC 250 walls, 250 slab; inside RCC {rx1 - rx0:.0f} × {2 * ry:.0f}, clear chamber 6,000 × 7,500 × 1,400 after the 100 mm lining",
          src="Rev H · HDG · D-11 · D-14", status="D")
    pockets, lids = [], []
    for sy in (1, -1):
        y0, y1 = sorted((sy * oy, sy * (oy + 1000)))
        pockets.append(box(-5600, -4400, y0, y1, -1200, 0).cut(box(-5400, -4600, min(sy * (oy - 1), sy * (oy + 800)), max(sy * (oy - 1), sy * (oy + 800)), -1000, 1)))
        lids.append(box(-5400, -4600, min(sy * oy, sy * (oy + 800)), max(sy * oy, sy * (oy + 800)), 0, 8))
    R.add("CIV-21 Chain-drive pockets", compound(*pockets), "civil", "rccpit", tag="CIV-21", title="Chain-drive pockets (north and south)",
          spec="800 × 800 × 1,000 clear each, RCC 200, drained; one per chain strand so each strand has its own drive (D-28)", material="RCC M25",
          src="this design · D-28", status="D", qty="2")
    R.add("CIV-21a Pocket lids", compound(*lids), "civil", "deck", tag="CIV-21a", title="Chequered pocket lids", spec="8 mm chequered plate, hinged, padlockable",
          src="this design", status="D", qty="2")
    lin = box(rx0, rx1, -ry, ry, zf - li, 0).cut(box(X0, X1, -Y, Y, zf, 1))
    for xa, xb, w in ((rx0 - 1, X0 + 1, 500), (X1 - 1, rx1 + 1, 450)):
        lin = lin.cut(box(xa, xb, -w, w, -1000, -300))
    R.add("DRY-10 Pit lining", lin, "dryer", "alu", tag="DRY-10", title="Dryer pit lining",
          spec="100 mm ceramic-fibre board 1260 grade on SS 304 M6 studs @ 400 × 400 with Ø40 speed washers, 1 mm aluminium liner pop-riveted; RCC face ≈62 °C (C-04)",
          material="Ceramic-fibre board 300 kg/m³; aluminium 1100-H14", src="D-14", status="D")
    # ---- top: perimeter curb, raised centre fixed cover (bridge) over P2-P3, two sliding doors that park under it (D-28)
    zc_top = 200                                       # curb top
    yr = 3800                                          # door rails
    xp1, xp4 = -9000, -6000                            # pinions (fixed), each under its door through the whole travel
    curb = box(ox0, ox1, -oy, oy, 0, zc_top).cut(box(-10350, -4650, -Y, Y, -1, zc_top + 1))
    for xp in (xp1, xp4):
        curb = curb.cut(box(xp - 80, xp + 80, 3800, 3900, 100, zc_top + 1)).cut(box(xp - 25, xp + 25, 3800, oy + 1, 160, zc_top + 1))
    R.add("DRY-11 Perimeter curb deck", curb, "dryer", "insul", tag="DRY-11", title="Insulated perimeter curb deck",
          spec="200 mm steel-framed curb on the pit walls (ISMC 200 frame, 150 mm mineral wool 96 kg/m³, 3 mm chequered top, 1 mm aluminium soffit); "
               "openings P1 (X −10.35 … −9.15) and P4 (X −5.85 … −4.65), 1,200 × 7,500; carries the door rails",
          material="IS 2062 E250; mineral wool", src="D-16 · D-28", status="D")
    bx0, bx1 = -9150, -5850
    bridge = box(bx0, bx1, -oy, oy, 550, 800)
    lips = [box(bx0, bx0 + 50, -3850, 3850, 505, 550), box(bx1 - 50, bx1, -3850, 3850, 505, 550)]
    girders = [_hollow_box(bx0, bx1, sy * 3900, sy * oy, zc_top, 550, 8) for sy in (1, -1)]
    R.add("DRY-11a Raised centre fixed cover", merge(bridge, compound(*lips)), "dryer", "insul", tag="DRY-11a", title="Raised fixed cover over P2–P3 (door garage under it)",
          spec="3,300 × 8,200 × 250 insulated (200 mm mineral wool, 3 mm top, 1 mm aluminium soffit), underside +0.550; both sliding doors park beneath it; "
               "end lips to +0.505 with silicone brush seals wipe the door tops", material="IS 2062 E250; mineral wool; aluminium", src="Owner instruction 21 Nov · D-28", status="D")
    R.add("DRY-11b Cover girders", compound(*girders), "dryer", "steel", tag="DRY-11b", title="Fixed-cover box girders",
          spec="Fabricated box 200 × 350 × 8 along both long sides on the curb, enclose the door garage at the sides; door-drive shafts pass under them through the curb",
          material="IS 2062 E250", src="D-28", status="D", qty="2")
    rails = compound(*[box(ox0, ox1, s * yr - 20, s * yr + 20, zc_top, zc_top + 30) for s in (1, -1)])
    R.add("DRY-12 Door rails", rails, "dryer", "steel", tag="DRY-12", title="Door rails",
          spec="Flat bar 40 × 30 EN8 on the curb, full length both sides; north rail V-profile (guides the doors), south rail flat", material="EN8", src="SH-RBR-01/02 · D-28", status="C")
    trav = B.v("dryer.door_travel")
    for key, xa, d, label, xp in (("DRY-02", -10425, 1, "P1, entry; slides east under the fixed cover", xp1), ("DRY-03", -6125, -1, "P4, exit; slides west under the fixed cover", xp4)):
        xb = xa + 1550
        body = box(xa, xb, -3850, 3850, 260, 500)
        whx = (xa + 200, xb - 200)
        for x in whx:
            for s in (1, -1):
                body = body.cut(box(x - 90, x + 90, s * yr - 45, s * yr + 45, 259, 400))
        frame_ = box(xa, xb, -3850, 3850, 495, 500).union(box(xa, xb, -3850, 3850, 260, 265))
        wheels = [cyl((x, s * yr - 20, 300), (x, s * yr + 20, 300), 70) for x in whx for s in (1, -1)]
        axles = [cyl((x, s * yr - 45, 300), (x, s * yr + 45, 300), 20) for x in whx for s in (1, -1)]
        seals = [box(xa, xb, s * 3850, s * 3860, 270, 490) for s in (1, -1)] + [box(x0_, x0_ + 10, -3850, 3850, 270, 490) for x0_ in (xa - 10, xb)]
        rack = box(xa, xb, 3825, 3850, 235, 260)
        cam_x = xa - 110 if d > 0 else xb
        cam = box(cam_x, cam_x + 110, 3870, 3940, 290, 320).union(box(cam_x + (100 if d > 0 else 0), cam_x + (110 if d > 0 else 10), 3850, 3940, 290, 400))
        anim = f"dry{key[-1]}:{d * trav:.0f}"
        R.add(f"{key} Dryer door {label.split(',')[0]}", compound(merge(body, frame_), *wheels, *axles, *seals), "dryer", "alu", tag=key, title=f"Dryer door {label}",
              spec=f"1,550 × 7,700 × 240 insulated: RHS 100 × 100 × 4 box frame, 200 mm mineral wool 96 kg/m³, 1 mm aluminium skins; 4 Ø140 wheels in pockets "
                   f"(V-groove north, flat south) with anti-lift hooks; travel {trav:.0f} under the raised fixed cover; silicone seals on all edges; "
                   "interlocked with the chain (no index with a door open)", material="IS 4923 frame; aluminium 1100; mineral wool", src="SH-RBR-01/02 · HDG · D-28", status="D", anim=anim)
        R.add(f"{key}k Door rack and cam {label.split(',')[0]}", merge(rack, cam), "dryer", "gear", tag=f"{key}k", title=f"Door rack and limit cam ({label.split(',')[0]})",
              spec="Rack m6 1,550 × 25 × 60 EN8 (45–50 HRC teeth) under the north edge of the door only (one-side drive, D-28); cam plate for the four limit switches",
              material="EN8 induction hardened", src="SH-RBR-01/02 · D-28", status="C", anim=anim)
        pin = merge(cyl((xp, 3825, 181), (xp, 3850, 181), 54), cyl((xp, 3850, 181), (xp, oy + 150, 181), 18))
        gm = merge(box(xp - 220, xp + 220, oy + 20, oy + 500, 0, 20), box(xp - 130, xp + 130, oy + 150, oy + 450, 20, 330),
                   cyl((xp + d * 130, oy + 300, 175), (xp + d * 500, oy + 300, 175), 90), box(xp - 60, xp + 60, oy + 20, oy + 150, 120, 250))
        R.add(f"{key}r Door drive {label.split(',')[0]}", merge(pin, gm), "dryer", "motor", tag=f"{key}r", title=f"Door drive, one side only ({label.split(',')[0]})",
              spec="Pinion m6 16T PCD 96 EN19 on a Ø40 shaft through the curb to a BK50 bevel gearmotor 1.1 kW 4-pole 75.4:1 (19 rpm, 550 N·m) with brake on the north side; "
                   "eccentric backing roller keeps the rack in mesh; south side runs free on its rail (the box frame takes the skew)", src="SH-RBR-01/02 · D-28", status="C")
        if d > 0:
            sw_x = [-10525, -10325, -9440, -9240]
        else:
            sw_x = [-4475, -4675, -5560, -5760]
        sw = [box(min(sw_x) - 40, max(sw_x) + 40, 3940, 3990, zc_top, zc_top + 40)]
        for x in sw_x:
            sw += [box(x - 25, x + 25, 3945, 3985, zc_top + 40, zc_top + 140), cyl((x, 3945, zc_top + 120), (x, 3925, zc_top + 120), 6),
                   cyl((x, 3925, zc_top + 120), (x, 3925, zc_top + 160), 4), cyl((x, 3918, zc_top + 160), (x, 3932, zc_top + 160), 16)]
        ends = (xa - 60, -7540) if d > 0 else (xb + 10,)
        buf = [box(x, x + (80 if x == -7540 else 50), s * 3700, s * 3740, zc_top, zc_top + 120) for x in ends for s in (1, -1)]
        R.add(f"{key}L Door limit switches {label.split(',')[0]}", compound(*sw, *buf), "instr", "yellow", tag=f"{key}L", title=f"4 limit switches and end buffers ({label.split(',')[0]})",
              spec="Mounting bar L 50 × 50 × 6 on the north curb (in ambient air, clear of the garage), 4 heavy-duty roller-lever switches IP67: OPEN slow-down, OPEN stop, "
                   "CLOSE slow-down, CLOSE stop (200 apart at each end); rubber end buffers beyond each stop; switches wired to the PLC with the chain interlock",
              material="Switch: Omron D4A-4516N-F class, IP67", src="SH-RBR-01/02 · owner instruction 21 Nov · D-28", status="D", qty="4")
    # perforated boxes (D-12)
    for key, xa, xb, face_x, col, label, spec in (
            ("DRY-04", X0, X0 + 350, X0 + 350, "supp", "Perforated supply box", "centre fed through 1,000 × 700 from the discharge trench; feed 12.6 m/s, hole ΔP / feed VP = 2.05 (C-09)"),
            ("DRY-05", X1 - 350, X1, X1 - 350, "retn", "Perforated extraction box", "centre drawn into the 900 × 1,000 return trench")):
        bx = box(xa, xb, -3500, 3500, -1350, -50)
        R.add(f"{key} {label}", bx, "dryer", "galv", tag=key, title=label,
              spec="1,300 × 350 × 7,000; face 7,000 × 1,000 perforated Ø15 @ 37 staggered 60° (14.9 % open, ≈5,900 holes); " + spec,
              material="GI 2 mm, CNC turret punched, 4 sections of 1,750", src="D-12 · Rev H", status="D")
        R.add(f"{key}p {label} face", box(face_x - (2 if xa == X0 else -2), face_x + (2 if xa == X0 else -2) * 0 + (0 if xa == X0 else 0), -3500, 3500, -1200, -200).union(
            box(face_x - 3, face_x + 3, -3500, 3500, -1200, -200)), "dryer", col, tag=f"{key}p", title=f"{label}: perforated face",
            spec="Ø15 holes, 37 mm staggered pitch, 7,000 × 1,000", src="D-12", status="D", layer="perf")
    trs = merge(box(X0 - li - wl, X0, -500, 500, -1000, -300), box(X1, X1 + li + wl, -450, 450, -1000, -300))
    R.add("DRY-06 Wall transitions", trs, "dryer", "galv", tag="DRY-06", title="Supply and return transitions through the pit walls",
          spec="Supply 1,000 × 700; return 900 × 700; GI with flexible seal", src="D-12", status="D")
    # chain conveyor
    xh, xt, zc, R_s = -5000, -10000, -500, 150
    shafts = compound(*[cyl((xh, sy * 3500, zc), (xh, sy * 4700, zc), 35) for sy in (1, -1)], *[cyl((xt, sy * 3500, zc), (xt, sy * 3720, zc), 35) for sy in (1, -1)])
    takeups = compound(*[box(xt - 160, xt + 160, min(sy * 3640, sy * 3745), max(sy * 3640, sy * 3745), zc - 130, zc + 130) for sy in (1, -1)])
    spro, chain, rails2 = [], [], []
    for y in (-3550, 3550):
        for x in (xt, xh):
            d = cyl((x, y - 15, zc), (x, y + 15, zc), 172)
            spro.append(d)
        chain.append(box(xt, xh, y - 15, y + 15, zc + R_s - 12, zc + R_s + 12))
        chain.append(box(xt, xh, y - 15, y + 15, zc - R_s - 12, zc - R_s + 12))
        for x in (xt, xh):
            chain.append(cyl((x, y - 15, zc), (x, y + 15, zc), R_s + 12).cut(cyl((x, y - 16, zc), (x, y + 16, zc), R_s - 12)).intersect(
                box(x if x == xh else x - 200, x + 200 if x == xh else x, y - 20, y + 20, zc - 200, zc + 200)))
        rails2.append(box(xt + 150, xh - 150, y - 45, y + 45, zc + R_s - 57, zc + R_s - 12))
        rails2.append(box(xt + 150, xh - 150, y - 45, y + 45, zc - R_s - 57, zc - R_s - 12))
        for x in range(int(xt) + 400, int(xh), 1200):
            rails2.append(box(x - 30, x + 30, y - 30, y + 30, zf, zc - R_s - 57))
    R.add("DRY-07 Chain conveyor", compound(*chain), "dryer", "chain", tag="DRY-07", title="Two-strand chain conveyor",
          spec="Roller chain, 2 strands at Y ±3,550, head/tail at X −5.0 / −10.0 m; indexes one position (1,500) per pulse; hard stop at P4",
          src="HDG · dryer instrumentation notes", status="C")
    R.add("DRY-08 Sprockets and stub shafts", merge(compound(*spro), shafts, takeups), "dryer", "gear", tag="DRY-08", title="Sprockets 12T PCD 300 on independent stub shafts",
          spec="12T PCD 300 keyed; head shafts Ø70 split per strand, each through its own side wall to its own drive pocket (no line shaft across the chamber, D-28); "
               "tail sprockets on stub shafts in screw take-ups (±75) inside the lining", material="EN8 shafts; C45 sprockets", src="HDG · D-28", status="D")
    R.add("DRY-09 Chain guides", compound(*rails2), "dryer", "steel", tag="DRY-09", title="Chain guide rails and return shoes", spec="UHMW wear strip on angle; posts @ 1,200", src="HDG", status="C")
    sad = compound(*[box(x - 140, x + 140, y - 70, y + 70, zc + R_s + 12, zc + R_s + 152) for x in g.dP for y in (-3550, 3550)])
    R.add("DRY-13 Saddles", sad, "dryer", "steel", tag="DRY-13", title="Chain saddles (jig ends ride on them)", spec="4 pairs at P1–P4, 1,500 pitch", src="HDG", status="C")
    gms = []
    for sy in (1, -1):
        y = lambda d: sy * d
        gms += [box(-5300, -4700, min(y(4200), y(4750)), max(y(4200), y(4750)), -1000, -900),
                box(-5200, -4800, min(y(4350), y(4650)), max(y(4350), y(4650)), -900, -520),
                cyl((-5000, y(4200), -500), (-5000, y(4350), -500), 160), cyl((-5000, y(4650), -500), (-5000, y(4720), -500), 60)]
    R.add("DRY-14 Chain drives (one per strand)", compound(*gms), "dryer", "motor", tag="DRY-14", title="Chain drives: one gearmotor per strand",
          spec="2 × 3.7 kW helical-bevel gearmotors, one in each side pocket on its own head stub shaft (D-28); each on a VFD with an encoder, run as an electronic "
               "line shaft (master/follower) so both strands index together; skew trip if the strands differ by > 10 mm at P4; timed pulses from the PLC",
          src="Owner instruction 21 Nov · D-28 · dryer instrumentation notes", status="D", qty="2")
    tw = merge(cyl((-7500, 3000, 800), (-7500, 3000, -750), 10), box(-7560, -7440, 2940, 3060, 800, 890))
    btn = merge(box(ox0 - 300, ox0 - 150, -oy - 300, -oy - 150, 0, 1200), box(ox0 - 290, ox0 - 160, -oy - 310, -oy - 290, 1000, 1100))
    wx = g.dP[3] - 100
    whisk = merge(box(wx - 50, wx + 50, Y - 10, Y, 20, 190), box(wx - 20, wx + 20, Y - 110, Y - 10, 120, 140), box(wx - 30, wx + 30, Y - 110, Y - 60, 140, 230),
                  cyl((wx, Y - 85, 120), (wx, Y - 85, -100), 2), sph((wx, Y - 85, -100), 6))
    R.add("DRY-15 Dryer Pt100", tw, "instr", "galv", tag="DRY-15", title="Dryer temperature Pt100", spec="Duplex Pt100 Class A, Ø8 SS316, 1,000 insertion, through the fixed cover", src="Dryer instrumentation notes", status="C")
    R.add("DRY-16 P1 LOADED station", btn, "instr", "yellow", tag="DRY-16", title="P1 LOADED pushbutton station",
          spec="Pedestal station at the SW corner: P1 LOADED (green), CHAIN STOP (red), key switch for manual index", src="Dryer instrumentation notes", status="C")
    R.add("DRY-17 P4 cat-whisker switch", whisk, "instr", "yellow", tag="DRY-17", title="P4 arrival: cat-whisker switch on a wall cantilever",
          spec="Spring-rod (cat-whisker) limit switch, any-direction actuation, on a 100 mm cantilever bracket from the north wall top at X −5.35; the Ø3 SS whisker hangs to −0.100 "
               "in the path of the jig-beam end and trips 100 before P4; head rated 150 °C, cable in SS conduit to a JB outside", material="Switch head high-temperature (A); bracket SS 304",
          src="Owner instruction 21 Nov · D-28", status="D")
    R.add("FLOW-dryer Dryer air", box(X0 + 350, X1 - 350, -3500, 3500, -1250, -150), "dryer", "supp", tag="FLOW", title="Drying air 120 → 100 °C",
          spec="11.44 m³/s cross-flow ≈1.6 m/s through all four loads; ≈209 kW (C-08)", src="Rev H · C-08", status="C", alpha=0.18, layer="flow")


def _hollow_box(x0, x1, y0, y1, z0, z1, t):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    return box(x0, x1, y0, y1, z0, z1).cut(box(x0 - 1, x1 + 1, y0 + t, y1 - t, z0 + t, z1 - t))


def build_stack(R):
    g = G
    bx, by = g.bleed
    sx, sy = g.stack
    riser = pipe(g.bleed_route, 203)
    bd = merge(cyl((bx, by, 1940), (bx, by, 2060), 245), box(bx + 245, bx + 400, by - 40, by + 40, 1950, 2050))
    R.add("HRL-09 Bleed duct Ø400", riser, "stack", "bleed", tag="HRL-09", title="Bleed duct Ø400",
          spec="Out of the discharge trench just downstream of the blower; 4,729 Nm³/h = flue + fresh air (C-08), 15 m/s; open to the stack by geometry, never by a control action",
          src="Rev H · D-22 (route)", status="C")
    R.add("HRL-09a Balancing damper BD-1", bd, "stack", "red", tag="HRL-09a", title="Balancing damper BD-1", spec="Ø400 butterfly, 6 mm disc, locking quadrant, 120 °C", src="Rev H · BD-1/BD-2 notes", status="C")
    hxx = sx
    hx = merge(box(hxx - 550, hxx + 550, -11800, -10600, 3450, 4550), cyl((hxx + 550, -11000, 3700), (hxx + 800, -11000, 3700), 45), cyl((hxx + 550, -11400, 4300), (hxx + 800, -11400, 4300), 45))
    R.add("HRL-10 Flue-gas heat exchanger", hx, "stack", "steel2", tag="HRL-10", title="Flue-gas heat exchanger (hot water to flux and degreasing tanks)",
          spec="≈150 kW available in the bleed (C-08); closed hot-water loop with 3-way valve; optional in this scope", src="Rev H · SHIVAS flux tank heating", status="C")
    gp = lambda x, y, along_x: merge(box(x - 700, x - 600, y - 50, y + 50, 0, 3790), box(x + 600, x + 700, y - 50, y + 50, 0, 3790), box(x - 700, x + 700, y - 60, y + 60, 3690, 3790)) if not along_x else \
        merge(box(x - 50, x + 50, y - 700, y - 600, 0, 3790), box(x - 50, x + 50, y + 600, y + 700, 0, 3790), box(x - 60, x + 60, y - 700, y + 700, 3690, 3790))
    posts = compound(gp(-9500, -6100, True), gp(sx, -9000, False), gp(sx, -13300, False))
    R.add("HRL-11 Bleed duct supports", posts, "stack", "steel", tag="HRL-11", title="Goal-post supports for the bleed duct", spec="ISMB 100, at 3.7 m", src="this design", status="D")
    st = tube((sx, sy, 350), (sx, sy, 12000), 206, 200)
    base = merge(box(sx - 600, sx + 600, sy - 600, sy + 600, -500, 350), cyl((sx, sy, 350), (sx, sy, 370), 360))
    gus = compound(*[box(sx + 200 * math.cos(a) - 6 if abs(math.cos(a)) < .5 else sx + 200 * math.cos(a), sx + 350 * math.cos(a) + 6, sy - 6, sy + 6, 370, 620).rotate((sx, sy, 0), (sx, sy, 1), math.degrees(a)) for a in [k * math.pi / 4 for k in range(8)]])
    port = cyl((sx, sy + 200, 8000), (sx, sy + 350, 8000), 50)
    plat = merge(tube((sx, sy, 7700), (sx, sy, 7740), 1000, 210), *[cyl((sx + 1000 * math.cos(a), sy + 1000 * math.sin(a), 7740), (sx + 1000 * math.cos(a), sy + 1000 * math.sin(a), 8800), 20) for a in [k * math.pi / 4 for k in range(8)]],
                 tube((sx, sy, 8780), (sx, sy, 8810), 1010, 990))
    lad = compound(*[box(sx - 220 + d, sx - 200 + d, sy - 450, sy - 430, 370, 7700) for d in (0, 400)], *[cyl((sx - 200, sy - 440, z), (sx + 180, sy - 440, z), 10) for z in range(650, 7700, 300)])
    rod = cyl((sx, sy, 12000), (sx, sy, 13500), 10)
    R.add("STK-01 Stack Ø400 × 12 m", merge(st, rod), "stack", "bleed", tag="STK-01", title="Bleed stack Ø400 × 12 m",
          spec="6 mm MS, top +12.0; exit 15 m/s; draft ≈3 mmWC; lightning conductor; height to be confirmed against the SPCB consent (O-05)",
          src="HDG (single line) · Rev H (two lines → Ø600) · C-13", status="C")
    R.add("STK-02 Stack base", merge(base, gus), "stack", "concrete2", tag="STK-02", title="Stack foundation and base plate", spec="RCC 1,200 sq.; base plate Ø720 × 20 with 8 gussets", src="this design", status="D")
    R.add("STK-03 Sampling port and platform", merge(port, plat, lad), "stack", "galv", tag="STK-03", title="Sampling port, platform and ladder",
          spec="Ø100 port at +8.0 m; ring platform at +7.7 m with handrail; ladder", src="this design (CPCB practice)", status="D")
    R.add("FLOW-bleed Bleed gas", cyl((bx, by, -480), (bx, by, 3900), 150), "stack", "bleed", tag="FLOW", title="Bleed 120 °C", spec="4,729 Nm³/h", src="C-08", status="C", alpha=0.35, layer="flow")


def build_loads(R):
    g = G
    jigs = []
    for x in g.dP:
        zb = -350 + 150 + 12 + 152 - 12          # on the saddles
        zb = -500 + 150 + 12 + 140
        beam = box(x - 50, x + 50, -3700, 3700, zb, zb + 200)
        lugs = [box(x - 15, x + 15, y - 60, y + 60, zb + 200, zb + 320) for y in (-1600, 1600)]
        work = [box(x - 35, x + 35, y - 35, y + 35, zb - 1050, zb) for y in (-3000, -1000, 1000, 3000)]
        work += [box(x - 100, x + 100, -3200, 3200, zb - 1050 + k * 300, zb - 1000 + k * 300) for k in range(3)]
        work += [cyl((x, -3300, zb - 300), (x, 3300, zb - 300), 45)]
        jigs += [beam, *lugs, *work]
    R.add("JIG-01 Jigs in the dryer", compound(*jigs), "load", "work", tag="JIG-01", title="Jigs at P1–P4 (sample loads)",
          spec="Jig beam 7.4 m ISMB 200, lugs at ±1.6 m; work hung ≈1.05 m below the beam", src="HDG jig", status="C")
    # 1.75 m scale figures
    figs = []
    for (x, y, z) in ((600, 5200, g.bpit_floor), (-7500, -5200, 0), (2700, 2600, 0)):
        figs += [cyl((x - 90, y, z), (x - 90, y, z + 850), 60), cyl((x + 90, y, z), (x + 90, y, z + 850), 60),
                 box(x - 190, x + 190, y - 110, y + 110, z + 850, z + 1450), sph((x, y, z + 1600), 120)]
    R.add("REF-01 Scale figures 1.75 m", compound(*figs), "load", "yellow", tag="REF-01", title="Scale figures (1.75 m)", spec="For scale only", src="—", status="C")


def build(R):
    build_flue(R)
    build_trenches(R)
    build_mixing_box(R)
    build_blower(R)
    build_dryer(R)
    build_stack(R)
    from .enclosure import build_enclosure
    build_enclosure(R)
    build_loads(R)
