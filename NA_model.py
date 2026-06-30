"""
Visual for the "missing cone" effect.
Each transverse frequency q_perp = |q_x| (the frequency space for the problem is symetric so taking a single quarter slice where q_y = 0 is just as general) 
is scanned for t = k_ix on all valid angles according to instrumental limits set by NA_ill and NA_obj,
then an enveloppe is computed on [qz_min(q_perp), qz_max(q_perp)] such that
 q_z = sqrt(k0^2 - ksx^2) - sqrt(k0^2 - kix^2) is verified, which is only defined inside of physical constraints set by Ewald spheres of radius k0.

The enveloppe shrinks faster when q_perp -> 0 as NA_ill << NA_obj
which geometrically defines the missing cone.

In your terminal with the proper env activated, run:
    python missing_cone_dpc.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

LAMBDA = 0.5  # longueur d'onde en microns (fixe)
N_QPERP = 240  # resolution de l'axe q_perp
N_T = 200       # resolution du balayage sur t = k_ix


def compute_envelope(na_ill: float, na_obj: float, lam: float = LAMBDA):
    """
    Calcule l'enveloppe (qz_min, qz_max) en fonction de q_perp pour des NA donnes.

    Parametres
    ----------
    na_ill : NA d'illumination
    na_obj : NA de l'objectif
    lam    : longueur d'onde

    Retour
    ------
    q_perp : array des frequences transverses (1/microns)
    qz_min, qz_max : arrays des bornes de l'enveloppe (1/microns), np.nan si non atteignable
    """
    k0 = 1.0 / lam
    k_ill = na_ill / lam
    k_obj = na_obj / lam
    q_max = k_ill + k_obj  # plus grande frequence transverse atteignable

    q_perp = np.linspace(0.0, q_max, N_QPERP)
    qz_min = np.full_like(q_perp, np.nan)
    qz_max = np.full_like(q_perp, np.nan)

    for i, qx in enumerate(q_perp):
        # t = k_ix doit satisfaire |t| <= k_ill ET |t + qx| <= k_obj
        t_low = max(-k_ill, -k_obj - qx)
        t_high = min(k_ill, k_obj - qx)
        if t_low > t_high:
            continue  # aucune combinaison valide pour ce q_perp

        t_vals = np.linspace(t_low, t_high, N_T)
        ksx = t_vals + qx

        kix_sq = t_vals ** 2
        ksx_sq = ksx ** 2

        # ne garder que les valeurs physiquement valides (sous la sphere d'Ewald)
        valid = (kix_sq < k0 ** 2) & (ksx_sq < k0 ** 2)
        if not np.any(valid):
            continue

        qz_vals = np.sqrt(k0 ** 2 - ksx_sq[valid]) - np.sqrt(k0 ** 2 - kix_sq[valid])
        qz_min[i] = np.min(qz_vals)
        qz_max[i] = np.max(qz_vals)

    return q_perp, qz_min, qz_max


def main():
    na_ill_init = 0.30
    na_obj_init = 1.0

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(left=0.12, bottom=0.28, right=0.95, top=0.92)

    q_perp, qz_min, qz_max = compute_envelope(na_ill_init, na_obj_init)

    line_max, = ax.plot(q_perp, qz_max, color="#185FA5", lw=1.5, label=r"$q_z^{max}$")
    line_min, = ax.plot(q_perp, qz_min, color="#185FA5", lw=1.5, label=r"$q_z^{min}$")
    fill = ax.fill_between(q_perp, qz_min, qz_max, color="#85B7EB", alpha=0.4)

    ax.axhline(0, color="gray", lw=0.5, linestyle="--")
    ax.set_xlabel(r"$q_\perp = |q_x|$  ($\mu m^{-1}$)")
    ax.set_ylabel(r"$q_z$  ($\mu m^{-1}$)")
    ax.set_title("Enveloppe des fréquences accessibles — missing cone DPC")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.2)

    ratio_text = ax.text(
        0.02, 0.95,
        f"Incohérence NA_ill/NA_obj = {na_ill_init/na_obj_init:.2f}",
        transform=ax.transAxes, fontsize=10, va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="lightgray"),
    )

    # --- Sliders ---
    ax_naill = plt.axes([0.15, 0.14, 0.7, 0.03])
    ax_naobj = plt.axes([0.15, 0.08, 0.7, 0.03])

    s_naill = Slider(ax_naill, "NA illumination", 0.05, 1.0, valinit=na_ill_init, valstep=0.01)
    s_naobj = Slider(ax_naobj, "NA objectif", 0.05, 1.0, valinit=na_obj_init, valstep=0.01)

    def update(_):
        na_ill = s_naill.val
        na_obj = s_naobj.val
        q_perp, qz_min, qz_max = compute_envelope(na_ill, na_obj)

        line_max.set_data(q_perp, qz_max)
        line_min.set_data(q_perp, qz_min)

        # il faut retirer et recreer le fill_between (pas de .set_data dispo)
        nonlocal fill
        fill.remove()
        fill = ax.fill_between(q_perp, qz_min, qz_max, color="#85B7EB", alpha=0.4)

        ratio_text.set_text(f"Incohérence NA_ill/NA_obj = {na_ill/na_obj:.2f}")

        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()

    s_naill.on_changed(update)
    s_naobj.on_changed(update)

    plt.show()


if __name__ == "__main__":
    main()