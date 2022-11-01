from .mphys_group import MphysGroup

class Scenario(MphysGroup):
    """
    A group to represent a specific analysis condition or point of the Mphys
    multipoint groups.

    To make a Scenario for a particular type of multiphysics problem, subclass
    the Scenario, and implement the `initialize` and `setup` phases of the Group.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._post_subsystems = []

    def _mphys_add_pre_coupling_subsystem_from_builder(self, name, builder, scenario_name=None):
        """
        If the builder has a precoupling subsystem, add it to the model.
        It is expected that is method is called during this scenario's`setup` phase.

        Parameters
        ----------
        name: str
            Name of the discipline
        builder: :class:`~mphys.builder.Builder`
            The discipline's builder object
        scenario_name: str or None
            Name of the scenario being setup (optional)
        """
        subsystem = builder.get_pre_coupling_subsystem(scenario_name)
        if subsystem is not None:
            self.mphys_add_subsystem(name+'_pre', subsystem)

    def _mphys_add_post_coupling_subsystem_from_builder(self, name, builder, scenario_name=None):
        """
        If the builder has a postcoupling subsystem, add it to the model.
        It is expected that is method is called during this scenario's`setup` phase.

        Parameters
        ----------
        name: str
            Name of the discipline
        builder: :class:`~mphys.builder.Builder`
            The discipline's builder object
        scenario_name: str or None
            Name of the scenario being setup (optional)
        """
        subsystem = builder.get_post_coupling_subsystem(scenario_name)
        if subsystem is not None:
            self.mphys_add_subsystem(name+'_post', subsystem)

    def mphys_add_post_subsystem(self, name, subsystem, promotes=None):
        """
        Add a user-defined subsystem at the end of a Scenario.
        Tag variables with mphys tags to promote or use the optional promotes argument.

        Parameters
        ----------
        name: str
            Name of the subsystem
        subsystem: <System>
            The
        promotes: iter of (str or tuple), optional
            If None, variables will be promoted using mphys_* tags,
            else variables will be promoted by this input
        """

        # we hold onto these until configure() b/c we want the scenario's
        # setup() to add the builder subsystems before adding these
        self._post_subsystems.append((name, subsystem, promotes))

    def configure(self):
        for name, subsystem, promotes in self._post_subsystems:
            if promotes is None:
                self.mphys_add_subsystem(name, subsystem)
            else:
                self.add_subsystem(name, subsystem, promotes=promotes)

        # tagged promotion
        super().configure()
