from pathlib import Path

import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.colors import LogNorm


TICKS = False
DESC = True
LAT_RA = [-10, 10]
OPTS = dict(cmap="inferno", aspect="auto")
FACECOLOR = "black"

DATA = {
    "Haslam et al.": "data/haslam408_dsds_Remazeilles2014.fits",
    "LAB HI Survey": "data/LAB_fullvel.fits",
    "Effelsberg/Parkes": [
        "data/spass_dr1_1902_healpix_Tb.i.fits",
        "data/EFFELSBERG_11cm_1_2048.fits",
    ],
    "Dame et al.": "data/lambda_wco_dht2001.fits",
    "IRIS": [
        "data/IRIS_nohole_4_2048_v2.fits",
        "data/IRIS_nohole_3_2048_v2.fits",
        "data/IRIS_nohole_1_1024_v2.fits",
    ],
    "GLIMPSE": "data/GLIMPSE_irac2_4arcm_1_2048_partial.fits",
    "DIRBE": [
        "data/DIRBE_3_256.fits",
        "data/DIRBE_2_256.fits",
        "data/DIRBE_1_256.fits",
    ],
    "WHAM, VTSS and SHASSA": "data/Halpha_fwhm06_1024.fits",
    "GAIA": "data/1567215018536-ESA_Gaia_DR2_AllSky_Brightness_Colour_Cartesian_4000x2000.png",
    "Rosat": "data/RASS_SXRB_R5.fits",
    "Fermi": "preprocessed_data/lat_300mev_hpx.fits",
    "IceCube": "data/ic_2023_gal_neutrinos.csv",
}


def get_map_view(datafile: Path or str, latra: list = LAT_RA, icecube: bool = False):
    """
    Reads a (HEALPIX) FITS file and returns the
    map view.

    Parameters
    ----------
    datafile : Path or str
        Path to the FITS data file.

    Returns
    -------
    map_view : np.ndarray, shape(M,N)
        Cartesian map view of the sky map.
    """
    if isinstance(datafile, str):
        datafile = Path(datafile)

    if not datafile.is_file():
        raise FileNotFoundError(f"File {datafile} not found!")

    if not icecube:
        map = hp.read_map(datafile)

    else:
        map = np.genfromtxt(
            datafile,
            delimiter=",",
            skip_header=1,
            names=[
                "pixel",
                "ra(radians)",
                "dec(radians)",
                "mlog10p",
                "nsigma",
                "gamma",
            ],
        )
        map = map["nsigma"]

    map_view = hp.cartview(
        map,
        coord=["G"] if not icecube else "CG",
        latra=latra,
        cbar=None,
        title=None,
        return_projected_map=True,
    )

    return map_view[::-1]


def plot_skymaps():
    """
    WIP, plots all skymaps.
    """
    fig, axs = plt.subplots(11, 1, figsize=(16, 12), layout="constrained")
    axs = axs.flatten()

    for ax in axs:
        ax.set_facecolor(FACECOLOR)

    axs[0].imshow(get_map_view(DATA["Haslam et al."]), norm=LogNorm(10, 2e3), **OPTS)
    axs[1].imshow(
        get_map_view(DATA["LAB HI Survey"]), vmin=1e-2, vmax=8, norm=None, **OPTS
    )

    axs[2].imshow(
        get_map_view(DATA["Effelsberg/Parkes"][0]), norm=LogNorm(0.1, 1e1), **OPTS
    )
    axs[2].imshow(
        get_map_view(DATA["Effelsberg/Parkes"][1]), norm=LogNorm(1, 1e4), **OPTS
    )
    axs[2].fill_between(
        np.linspace(*axs[2].get_xlim(), 1000), -0.5, 10.5, color=FACECOLOR
    )
    axs[2].fill_between(
        np.linspace(*axs[2].get_xlim(), 1000), 32.5, 43.5, color=FACECOLOR
    )

    axs[3].imshow(get_map_view(DATA["Dame et al."]), norm=LogNorm(0.8, 1e2), **OPTS)

    iris = (
        get_map_view(DATA["IRIS"][0])
        + get_map_view(DATA["IRIS"][1])
        + get_map_view(DATA["IRIS"][2])
    )
    axs[4].imshow(iris, norm=LogNorm(2, 1e3), **OPTS)

    dirbe = (
        get_map_view(DATA["DIRBE"][0])
        + get_map_view(DATA["DIRBE"][1])
        + get_map_view(DATA["DIRBE"][2])
    )
    axs[5].imshow(dirbe, norm=LogNorm(0.5, 5e1), **OPTS)

    axs[6].imshow(
        get_map_view(DATA["WHAM, VTSS and SHASSA"]), norm=LogNorm(1, 1e3), **OPTS
    )

    gaia_img = imread(DATA["GAIA"])
    axs[7].imshow(gaia_img[900:1100, :, :], aspect="auto")
    axs[8].imshow(get_map_view(DATA["Rosat"]), norm=LogNorm(10, 2e3), **OPTS)
    axs[9].imshow(get_map_view(DATA["Fermi"]), norm=LogNorm(50, 5e3), **OPTS)
    axs[10].imshow(get_map_view(DATA["IceCube"], icecube=True), **OPTS)

    title = [
        "Haslam et al. (408 MHz)",
        "LAB HI Survey (Atomic Hydrogen, 21cm)",
        "Effelsberg/Parkes (2.4-2.7 GHz)",
        "Dame et al. (Molecular Hydrogen)",
        "IRIS (100, 60, 12 Microns IR)",
        "DIRBE (3.5, 2.5, 1.25 Microns NIR)",
        "WHAM, VTSS and SHASSA (H-Alpha)",
        "GAIA (Optical)",
        "Rosat (X-ray)",
        "Fermi (Gamma)",
        "IceCube 2023 (Neutrinos)",
    ]

    l0, l1 = axs[0].get_xlim()
    b0, b1 = axs[0].get_ylim()
    gaia_l0, gaia_l1 = axs[-4].get_xlim()
    gaia_b0, gaia_b1 = axs[-4].get_ylim()

    lon = np.linspace(l0, l1, 13)
    lat = np.linspace(b0, b1, 3)
    gaia_lon = np.linspace(gaia_l0, gaia_l1, 13)
    gaia_lat = np.linspace(gaia_b0, gaia_b1, 3)

    for ax, ttl in zip(axs, title):
        if DESC:
            ax.text(
                0.01,
                0.9,
                ttl,
                color="white",
                ha="left",
                va="top",
                transform=ax.transAxes,
            )
        ax.tick_params(labelright=True, right=True, top=True)
        if TICKS:
            ax.set(
                xticks=(lon) if not ttl == "GAIA (Optical)" else (gaia_lon),
                yticks=(lat) if not ttl == "GAIA (Optical)" else (gaia_lat),
                xticklabels=[
                    "180°",
                    "150°",
                    "120°",
                    "90°",
                    "60°",
                    "30°",
                    "0°",
                    "30°",
                    "60°",
                    "90°",
                    "120°",
                    "150°",
                    "180°",
                ],
                yticklabels=["-15°", "0°", "15°"],
            )
            ax.grid(False)
        else:
            ax.set(xticks=([]), yticks=([]), xticklabels="", yticklabels="")

    fig.savefig("build/multi_messenger.pdf", bbox_inches="tight")


if __name__ == "__main__":
    plot_skymaps()
