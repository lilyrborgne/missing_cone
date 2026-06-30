### Matplotlib implementation to visualise the recoverable frequency space for an imaging system with multiplexed illumination where the NA of illumination and the NA of the objective is known. 

## Required packages: 
- numpy
- matplotlib.pyplot
- matplotlib.widgets.Slider

The enveloppe features a quarter of a 2D slice of the recoverable frequencies space. However since the total dome of aggregated caps of Ewald spheres provided by the LEDs has the symetries of a sphere, that illustration embeds all the necessary information to model the missing cone. 

## It is based on the following equations:

*The definition of the sample's scattering vectors*

$\vec{q} = \vec{k_s}-\vec{k_i}$ **(1)**
where ks is a scattered wave vector and ki an incident wave vector

*The definition of an Ewald sphere, which delimitates the scattered frequency space*

$\sqrt{k_{sx}^2 + k_{sy}^2 + k_{sz}^2} = \frac{1}{\lambda}$  **(2)**

*The expression of energy conservation of light, which applies to the diffusion of the incident wave vector*

$\sqrt{k_{ix}^2 + k_{iy}^2 + k_{iz}^2} = \frac{1}{\lambda}$  **(3)**

*The restriction in scattering divergence from the axial direction "cookie-cutter"*

$\sqrt{k_{sx}^2 + k_{sy}^2} <= \frac{NA_{obj}}{\lambda}$ **(4)**

where $k_{sx}$ and $k_{sy}$ are the components of a scattered wave vector along x and y axes, $NA_{obj}$ is the numerical aperture of the objective and $\lambda$ the illumination wavelength. 

From **(2)** and  **(3)** imputed in **(1)** we obtain:

$\vec{q_z} = \sqrt{\frac{1}{\lambda}^2 - k_{sx}^2 - k_{sy}^2} - \sqrt{\frac{1}{\lambda}^2 - k_{ix}^2 - k_{iy}^2}$

And $\vec{q_x} = k_{sx} - k_{ix}$ which implies $|\vec{q_x}| <= (NA_{obj} + NA_{ill})/\lambda$





