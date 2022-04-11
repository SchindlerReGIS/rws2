import pathlib
import unittest

import numpy as np

from arco.learning_from_demo.probabilistic_encoding import ProbabilisticEncoding
from arco.learning_from_demo.trajectories import Trajectories
from arco.learning_from_demo.gaussian_mixture_regression import GMR


class ProbabilisticEncodingTest(unittest.TestCase):

    @staticmethod
    def _create_trajectory_and_prob_encoding() -> tuple[
        Trajectories, ProbabilisticEncoding
    ]:
        base_path = pathlib.Path(__file__).parent.absolute()
        data_path = str(pathlib.Path(base_path, "data"))
        trajectories = Trajectories.from_dataset_file(data_path)
        pe = ProbabilisticEncoding(
            trajectories,
            max_nb_components=10,
            min_nb_components=2,
            iterations=1,
            random_state=0,
        )
        return trajectories, pe

    def test_probabilistic_encoding(self):

        _, pe = self._create_trajectory_and_prob_encoding()
        # check best number GMM components
        self.assertEqual(pe.gmm.n_components, 3)
        # check norm of covariance matrices
        for i, norm in enumerate([249, 341, 308]):
            self.assertEqual(int(np.linalg.norm(pe.gmm.covariances_[i])), norm)

    def test_gmr_implementation(self):

        traj, pe = self._create_trajectory_and_prob_encoding()
        # compute regression curve
        regression = GMR(traj, pe)
        # check prediction vector, first timestamp
        self.assertTrue(
            np.allclose(
                regression.prediction[0, :],
                np.array(
                    [
                        0.0,
                        4.516551,
                        -31.69882542,
                        73.77655872,
                        9.95006722,
                        -48.19025304,
                        -10.81080946,
                    ]
                ),
            )
        )
        # check prediction vector, last timestamp
        self.assertTrue(
            np.allclose(
                regression.prediction[-1, :],
                np.array(
                    [
                        10.26,
                        15.80567897,
                        32.30803174,
                        13.01057104,
                        17.39767237,
                        -49.55641484,
                        -16.30629655,
                    ]
                ),
            )
        )
