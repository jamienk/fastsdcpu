from ...configuration_utils import PretrainedConfig


class PanConfig(PretrainedConfig):
    model_type = 'PAN'

    def __init__(self, scale=None, in_nc=3, out_nc=3, nf=40, unf=24, nb=16, bam=False,
                 data_parallel=False, **kwargs):
        super().__init__(**kwargs)
        self.scale = scale
        self.in_nc = in_nc
        self.out_nc = out_nc
        self.nf = nf
        self.unf = unf
        self.nb = nb
        self.data_parallel = data_parallel
        self.bam = bam
