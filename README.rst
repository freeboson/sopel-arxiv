
``sopel`` arXiv Module
----------------------
Simple IRC-arXiv interface via the ``sopel`` (<https://sopel.chat>`_) bot. It
will trigger on arXiv URLs for papers, as well as the common arXiv ID notation,
fetching the paper title, author information, and first few words of the
abstract. You can also use a command to search the arXiv, using their search
syntax, where it will give you the same info for the first result.

Installation
------------
Just put ``arxiv.py`` into one of the appropriate ``modules`` directories for
your bot, e.g. ``~/.sopel/modules``.

Examples
--------
Basic usage (my ``sopel`` bot is ``dirac`` on freenode)::

<sujeet> .help arxiv
<dirac> sujeet: e.g. .arxiv 1304.5526
<sujeet> .arxiv 1304.5526
<dirac> [arXiv:1304.5526] Sujeet Akula and Pran Nath, "Gluino-driven Radiative Breaking, Higgs Boson Mass, Muon $\mathbf{g-2}$,  and the Higgs Diphoton Decay in SUGRA Unification" :: We attempt to reconcile seemingly conflicting experimental results on the Higgs boson ma[…] http://arxiv.org/abs/1304.5526v1
<sujeet> .arxiv au:randall "out of this world"
<dirac> [arXiv:hep-th/9810155] Lisa Randall and Raman Sundrum, "Out Of This World Supersymmetry Breaking" :: We show that in a general hidden sector model, supersymmetry breaking necessarily generates at one-loop a scalar and gaugino mass as a consequence of the supe[…] http://arxiv.org/abs/hep-th/9810155v2
<sujeet> Did you guys see arxiv:hep-th/0503249? It looks fascinating!
<dirac> [arXiv:hep-th/0503249] P. J. Fox et al., "Supersplit Supersymmetry" :: The possible existence of an exponentially large number of vacua in string theory behooves one to consider possibilities beyond our traditional notions of naturalness. Such an approach to […] http://arxiv.org/abs/hep-th/0503249v2


