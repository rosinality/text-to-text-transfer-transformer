# Copyright 2023 The T5 Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Add Tasks to registry."""
# TODO(adarob): Switch to seqio.Task.

import functools

import seqio
import t5.data
from t5.data import postprocessors
from t5.data import preprocessors
from t5.data.glue_utils import get_glue_metric
from t5.data.glue_utils import get_glue_postprocess_fn
from t5.data.glue_utils import get_glue_text_preprocessor
from t5.data.glue_utils import get_super_glue_metric
from t5.evaluation import metrics
import tensorflow_datasets as tfds

TaskRegistry = seqio.TaskRegistry
NUM_VAL_EXAMPLES = 2000

DEFAULT_OUTPUT_FEATURES = {
    "inputs": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=True,
        required=False),
    "targets": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=True)
}

DEFAULT_OUTPUT_FEATURES_V2 = {
    "inputs": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=False,
        required=False),
    "targets": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=True)
}

DEFAULT_OUTPUT_FEATURES_V3 = {
    "inputs": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=False,
        required=False),
    "targets": seqio.Feature(
        vocabulary=t5.data.get_default_vocabulary(), add_eos=False)
}


# ==================================== C4 ======================================
# Final pretraining task used in Raffel et al., 2019.
TaskRegistry.add(
    "c4_v220_span_corruption",
    source=seqio.TfdsDataSource(tfds_name="c4/en:3.0.1"),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.span_corruption,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# Baseline pretraining task used in Raffel et al., 2019.
TaskRegistry.add(
    "c4_v220_iid_denoising",
    source=seqio.TfdsDataSource(tfds_name="c4/en:3.0.1"),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.iid_denoising,
        seqio.preprocessors.append_eos_after_trim,
    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# Prefix language modeling pretraining task used in Raffel et al., 2019.
TaskRegistry.add(
    "c4_v220_prefix_lm",
    source=seqio.TfdsDataSource(tfds_name="c4/en:3.0.1"),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.prefix_lm,
        seqio.preprocessors.append_eos_after_trim,
    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# Full language modeling pretraining task used in Raffel et al., 2019.
TaskRegistry.add(
    "c4_v220_full_lm",
    source=seqio.TfdsDataSource(tfds_name="c4/en:3.0.1"),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,
    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# UL2
TaskRegistry.add(
    "c4_v220_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="c4/en:3.0.1",
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "c4_v220_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="c4/en:3.0.1",
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])




# ========================OpenMoE Dataset=========================
TaskRegistry.add(
    "redpajama_stackexchange_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_stackexchange:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "redpajama_stackexchange_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_stackexchange:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# wiki dataset UL2
TaskRegistry.add(
    "redpajama_wikipedia_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_wikipedia:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "wikipedia_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="wikipedia/20190301.en:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])



TaskRegistry.add(
    "redpajama_wikipedia_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_wikipedia:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# C4 dataset UL2
TaskRegistry.add(
    "redpajama_c4_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_c4:1.0.0",
        splits={
            # 'train': 'train',
            'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "redpajama_c4_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_c4:1.0.0",
        splits={
            # 'train': 'train',
            'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# ArXiv dataset UL2
TaskRegistry.add(
    "redpajama_arxiv_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_arxiv:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "redpajama_arxiv_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_arxiv:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# Github dataset UL2
TaskRegistry.add(
    "redpajama_github_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_github:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "redpajama_github_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_github:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# Book dataset UL2
TaskRegistry.add(
    "redpajama_book_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_book:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "redpajama_book_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_book:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# Commoncrawl dataset UL2
TaskRegistry.add(
    "redpajama_common_crawl_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_common_crawl:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "redpajama_common_crawl_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_common_crawl:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# The Stack dataset UL2
TaskRegistry.add(
    "the_stack_dedup_ul2",
    source=seqio.TfdsDataSource(
        tfds_name="the_stack_dedup:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

TaskRegistry.add(
    "the_stack_dedup_ul2_noprefix",
    source=seqio.TfdsDataSource(
        tfds_name="the_stack_dedup:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective_noprefix,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])



# ========================OpenLLaMA Dataset=========================


TaskRegistry.add(
    "wikipedia_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="wikipedia/20190301.en:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])



TaskRegistry.add(
    "redpajama_stackexchange_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_stackexchange:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# wiki dataset UL2
TaskRegistry.add(
    "redpajama_wikipedia_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_wikipedia:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# C4 dataset UL2
TaskRegistry.add(
    "redpajama_c4_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_c4:1.0.0",
        splits={
            # 'train': 'train',
            'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# ArXiv dataset UL2
TaskRegistry.add(
    "redpajama_arxiv_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_arxiv:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# Github dataset UL2
TaskRegistry.add(
    "redpajama_github_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_github:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# Book dataset UL2
TaskRegistry.add(
    "redpajama_book_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_book:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# Commoncrawl dataset UL2
TaskRegistry.add(
    "redpajama_common_crawl_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="redpajama_common_crawl:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# The Stack dataset UL2
TaskRegistry.add(
    "the_stack_dedup_full_lm",
    source=seqio.TfdsDataSource(
        tfds_name="the_stack_dedup:1.0.0",
        splits={
            'train': 'train',
            # 'train': f'train[:-{NUM_VAL_EXAMPLES}]',
            # 'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.full_lm,
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])

# The Stack dataset UL2
TaskRegistry.add(
    "orca_sft",
    source=seqio.TfdsDataSource(
        tfds_name="orca:1.0.0",
        splits={
            'train': 'train',
            'validation': f'train[-{NUM_VAL_EXAMPLES}:]',
        },
    ),
    preprocessors=[
        preprocessors.orca_sft,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
    metric_fns=[])

TaskRegistry.add(
    "wildchat_gpt4_sft",
    source=seqio.TfdsDataSource(
        tfds_name="wildchat_gpt4_sft:1.0.0",
        splits={
            'train': 'train',
            'validation': f'train[-128:]',
        },
    ),
    preprocessors=[
        preprocessors.wildchat_sft,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES_V3,
    metric_fns=[])

TaskRegistry.add(
    "wildchat_gpt4_eval",
    source=seqio.TfdsDataSource(
        tfds_name="wildchat_gpt4_sft:1.0.0",
        splits={
            'validation': f'train[-256:]',
        },
    ),
    preprocessors=[
        preprocessors.wildchat_sft,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,

    ],
    output_features=DEFAULT_OUTPUT_FEATURES_V3,
    metric_fns=[metrics.accuracy],
)


# Configurable tasks used for comparisons in Raffel et al., 2019.
_c4_config_suffixes = ["", ".noclean", ".realnewslike", ".webtextlike"]
for config_suffix in _c4_config_suffixes:
  TaskRegistry.add(
      "c4{name}_v020_unsupervised".format(name=config_suffix.replace(".", "_")),
      source=seqio.TfdsDataSource(tfds_name="c4/en{config}:3.0.1".format(
          config=config_suffix)),
      preprocessors=[
          functools.partial(
              preprocessors.rekey, key_map={
                  "inputs": None,
                  "targets": "text"
              }),
          seqio.preprocessors.tokenize,
          seqio.CacheDatasetPlaceholder(),
          preprocessors.unsupervised,
          seqio.preprocessors.append_eos_after_trim,
      ],
      output_features=DEFAULT_OUTPUT_FEATURES,
      metric_fns=[])


# ================================ Wikipedia ===================================
TaskRegistry.add(
    "wikipedia_20190301.en_v003_unsupervised",
    source=seqio.TfdsDataSource(tfds_name="wikipedia/20190301.en:1.0.0"),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.unsupervised,
        seqio.preprocessors.append_eos_after_trim,
    ],
    output_features=DEFAULT_OUTPUT_FEATURES,
    metric_fns=[])


# =================================== GLUE =====================================
for b in tfds.text.glue.Glue.builder_configs.values():
  TaskRegistry.add(
      "glue_%s_v002" % b.name,
      source=seqio.TfdsDataSource(
          tfds_name="glue/%s:1.0.0" % b.name,
          splits=["test"] if b.name == "ax" else None),
      preprocessors=[
          get_glue_text_preprocessor(b),
          seqio.preprocessors.tokenize,
          seqio.CacheDatasetPlaceholder(),
          seqio.preprocessors.append_eos_after_trim,
      ],
      metric_fns=get_glue_metric(b.name),
      output_features=DEFAULT_OUTPUT_FEATURES,
      postprocess_fn=get_glue_postprocess_fn(b))

# =============================== CNN DailyMail ================================
TaskRegistry.add(
    "cnn_dailymail_v002",
    source=seqio.TfdsDataSource(tfds_name="cnn_dailymail:3.4.0"),
    preprocessors=[
        functools.partial(
            preprocessors.summarize,
            article_key="article",
            summary_key="highlights"),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    metric_fns=[metrics.rouge],
    output_features=DEFAULT_OUTPUT_FEATURES)

# ==================================== WMT =====================================
# Format: year, tfds builder config, tfds version
b_configs = [
    ("14", tfds.translate.wmt14.Wmt14Translate.builder_configs["de-en"], "1.0.0"
    ),
    ("14", tfds.translate.wmt14.Wmt14Translate.builder_configs["fr-en"], "1.0.0"
    ),
    ("16", tfds.translate.wmt16.Wmt16Translate.builder_configs["ro-en"], "1.0.0"
    ),
    ("15", tfds.translate.wmt15.Wmt15Translate.builder_configs["fr-en"], "1.0.0"
    ),
    ("19", tfds.translate.wmt19.Wmt19Translate.builder_configs["de-en"], "1.0.0"
    ),
]

for prefix, b, tfds_version in b_configs:
  TaskRegistry.add(
      "wmt%s_%s%s_v003" % (prefix, b.language_pair[1], b.language_pair[0]),
      source=seqio.TfdsDataSource(tfds_name="wmt%s_translate/%s:%s" %
                                  (prefix, b.name, tfds_version)),
      preprocessors=[
          functools.partial(
              preprocessors.translate,
              source_language=b.language_pair[1],
              target_language=b.language_pair[0],
          ),
          seqio.preprocessors.tokenize,
          seqio.CacheDatasetPlaceholder(),
          seqio.preprocessors.append_eos_after_trim,
      ],
      metric_fns=[metrics.bleu],
      output_features=DEFAULT_OUTPUT_FEATURES)

# Special case for t2t ende.
b = tfds.translate.wmt_t2t.WmtT2tTranslate.builder_configs["de-en"]
TaskRegistry.add(
    "wmt_t2t_ende_v003",
    source=seqio.TfdsDataSource(tfds_name="wmt_t2t_translate/de-en:1.0.0"),
    preprocessors=[
        functools.partial(
            preprocessors.translate,
            source_language=b.language_pair[1],
            target_language=b.language_pair[0]),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    metric_fns=[metrics.bleu],
    output_features=DEFAULT_OUTPUT_FEATURES)

# ================================= SuperGlue ==================================
for b in tfds.text.super_glue.SuperGlue.builder_configs.values():
  # We use a simplified version of WSC, defined below
  if "wsc" in b.name:
    continue
  if b.name == "axb":
    glue_preprocessors = [
        functools.partial(
            preprocessors.rekey,
            key_map={
                "premise": "sentence1",
                "hypothesis": "sentence2",
                "label": "label",
                "idx": "idx",
            }),
        get_glue_text_preprocessor(b),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ]
  else:
    glue_preprocessors = [
        get_glue_text_preprocessor(b),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ]
  TaskRegistry.add(
      "super_glue_%s_v102" % b.name,
      source=seqio.TfdsDataSource(
          tfds_name="super_glue/%s:1.0.2" % b.name,
          splits=["test"] if b.name in ["axb", "axg"] else None),
      preprocessors=glue_preprocessors,
      metric_fns=get_super_glue_metric(b.name),
      output_features=DEFAULT_OUTPUT_FEATURES,
      postprocess_fn=get_glue_postprocess_fn(b))

  # Create SuperGLUE tasks with 1 sentinel token added.
  seqio.experimental.add_task_with_sentinels("super_glue_%s_v102" % b.name,
                                             num_sentinels=1)

# ======================== Definite Pronoun Resolution =========================
TaskRegistry.add(
    "dpr_v001_simple",
    source=seqio.TfdsDataSource(tfds_name="definite_pronoun_resolution:1.1.0"),
    preprocessors=[
        preprocessors.definite_pronoun_resolution_simple,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    metric_fns=[metrics.accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES)

# Create SuperGLUE tasks with 1 sentinel token added.
seqio.experimental.add_task_with_sentinels("dpr_v001_simple", num_sentinels=1)

# =================================== WSC ======================================
TaskRegistry.add(
    "super_glue_wsc_v102_simple_train",
    source=seqio.TfdsDataSource(
        tfds_name="super_glue/wsc.fixed:1.0.2", splits=["train"]),
    preprocessors=[
        functools.partial(preprocessors.wsc_simple, correct_referent_only=True),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    metric_fns=[],
    output_features=DEFAULT_OUTPUT_FEATURES)

# Create SuperGLUE tasks with 1 sentinel token added.
seqio.experimental.add_task_with_sentinels("super_glue_wsc_v102_simple_train",
                                           num_sentinels=1)

TaskRegistry.add(
    "super_glue_wsc_v102_simple_eval",
    source=seqio.TfdsDataSource(
        tfds_name="super_glue/wsc.fixed:1.0.2", splits=["validation", "test"]),
    preprocessors=[
        functools.partial(
            preprocessors.wsc_simple, correct_referent_only=False),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    postprocess_fn=postprocessors.wsc_simple,
    metric_fns=[metrics.accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES)
# Create SuperGLUE tasks with 1 sentinel token added.
seqio.experimental.add_task_with_sentinels("super_glue_wsc_v102_simple_eval",
                                           num_sentinels=1)

# =================================== WNLI =====================================
TaskRegistry.add(
    "glue_wnli_v002_simple_eval",
    source=seqio.TfdsDataSource(
        tfds_name="glue/wnli:1.0.0", splits=["validation", "test"]),
    preprocessors=[
        preprocessors.wnli_simple,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    postprocess_fn=postprocessors.wsc_simple,
    metric_fns=[metrics.accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES)

# =================================== Squad ====================================
# Maximized evaluation metrics over all answers.
TaskRegistry.add(
    "squad_v010_allanswers",
    source=seqio.TfdsDataSource(tfds_name="squad/v1.1:3.0.0"),
    preprocessors=[
        preprocessors.squad,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    postprocess_fn=postprocessors.qa,
    metric_fns=[metrics.squad],
    output_features=DEFAULT_OUTPUT_FEATURES)


# Maximized evaluation metrics over all answers.
TaskRegistry.add(
    "squad_v010_context_free",
    source=seqio.TfdsDataSource(tfds_name="squad/v1.1:3.0.0"),
    preprocessors=[
        functools.partial(preprocessors.squad, include_context=False),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    postprocess_fn=postprocessors.qa,
    metric_fns=[metrics.squad],
    output_features=DEFAULT_OUTPUT_FEATURES)

# Squad span prediction task instead of text.
TaskRegistry.add(
    "squad_v010_allanswers_span",
    source=seqio.TfdsDataSource(tfds_name="squad/v1.1:3.0.0"),
    preprocessors=[
        preprocessors.squad_span_space_tokenized,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    postprocess_fn=postprocessors.span_qa,
    metric_fns=[metrics.span_squad],
    output_features=DEFAULT_OUTPUT_FEATURES)

# Deprecated: Use `squad_v010_allanswers` instead.
TaskRegistry.add(
    "squad_v010",
    source=seqio.TfdsDataSource(tfds_name="squad/v1.1:3.0.0"),
    preprocessors=[
        preprocessors.squad,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos_after_trim,
    ],
    metric_fns=[metrics.squad],
    output_features=DEFAULT_OUTPUT_FEATURES)

# ================================= TriviaQA ===================================
TaskRegistry.add(
    "trivia_qa_v010",
    source=seqio.TfdsDataSource(tfds_name="trivia_qa/rc:1.1.0"),
    preprocessors=[
        preprocessors.trivia_qa,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.trivia_qa_truncate_inputs,
        seqio.preprocessors.append_eos_after_trim,
    ],
    metric_fns=[metrics.squad],
    output_features=DEFAULT_OUTPUT_FEATURES)

def _filter_trivia_qa(dataset):
  def my_fn(example):
    return 'value' in example['answer']
  return dataset.filter(my_fn)

def tqa_open_postprocessor(output_or_target, example=None, is_target=False):
  """Returns output as answer, or all answers if the full example is provided."""
  if is_target:
    return [a for a in example["answers"]]
  else:
    return output_or_target

TaskRegistry.add(
    "trivia_qa_v010_nocontext",
    source=seqio.TfdsDataSource(tfds_name="trivia_qa/unfiltered.nocontext:1.1.0",
                                splits={
                                    'validation': f'validation',
                                }),
    preprocessors=[
        _filter_trivia_qa,
        preprocessors.trivia_qa_nocontext,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        # seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.trivia_qa,
    metric_fns=[metrics.ul2_trivia_qa],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
)

TaskRegistry.add(
    "sft_trivia_qa_v010_nocontext",
    source=seqio.TfdsDataSource(tfds_name="trivia_qa/unfiltered.nocontext:1.1.0",
                                splits={
                                    'validation': f'validation[:128]',
                                }),
    preprocessors=[
        _filter_trivia_qa,
        preprocessors.sft_trivia_qa_nocontext,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        # seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.trivia_qa,
    metric_fns=[metrics.ul2_trivia_qa],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
)

TaskRegistry.add(
    "ul2_trivia_qa_v010_nocontext",
    source=seqio.TfdsDataSource(tfds_name="trivia_qa/unfiltered.nocontext:1.1.0",
                                splits={
                                    'validation': f'validation',
                                }),
    preprocessors=[
        _filter_trivia_qa,
        preprocessors.ul2_trivia_qa_nocontext,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.qa,
    metric_fns=[metrics.ul2_trivia_qa],
    output_features=DEFAULT_OUTPUT_FEATURES,
)


TaskRegistry.add(
    "trivia_qa_v010_nocontext_oneshot",
    source=seqio.TfdsDataSource(tfds_name="trivia_qa/unfiltered.nocontext:1.1.0",
                                splits={
                                    'validation': f'validation[:256]',
                                }),
    preprocessors=[
        _filter_trivia_qa,
        preprocessors.ul2_trivia_qa_nocontext_oneshot,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.qa,
    metric_fns=[metrics.ul2_trivia_qa],
    output_features=DEFAULT_OUTPUT_FEATURES,
)

TaskRegistry.add(
    "trivia_qa_v010_nocontext_fewshot",
    source=seqio.TfdsDataSource(tfds_name="trivia_qa/unfiltered.nocontext:1.1.0",
                                splits={
                                    'validation': f'validation[:256]',
                                }),
    preprocessors=[
        _filter_trivia_qa,
        preprocessors.ul2_trivia_qa_nocontext_fewshot,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.qa,
    metric_fns=[metrics.ul2_trivia_qa],
    output_features=DEFAULT_OUTPUT_FEATURES,
)


# ==================================MMLU==================================

TaskRegistry.add(
    "mmlu",
    source=seqio.TfdsDataSource(tfds_name="mmlu:1.0.0",
                                splits={
                                    'validation': f'train[:128]',
                                }),
    preprocessors=[
        preprocessors.mmlu,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    metric_fns=[metrics.mmlu_accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
)

TaskRegistry.add(
    "ul2_mmlu",
    source=seqio.TfdsDataSource(tfds_name="mmlu:1.0.0",
                                splits={
                                    'validation': f'train',
                                }),
    preprocessors=[
        preprocessors.mmlu,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    metric_fns=[metrics.mmlu_accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES,
)

TaskRegistry.add(
    "sft_mmlu",
    source=seqio.TfdsDataSource(tfds_name="mmlu:1.0.0",
                                splits={
                                    'validation': f'train[:128]',
                                }),
    preprocessors=[
        preprocessors.sft_mmlu,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    metric_fns=[metrics.mmlu_accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
)


# ==================================LAMBADA==================================

TaskRegistry.add(
    "lambada",
    source=seqio.TfdsDataSource(tfds_name="lambada:1.0.0",
                                splits={
                                    'validation': f'test',
                                }),
    preprocessors=[
        preprocessors.lambada,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.take_first_word,
    metric_fns=[metrics.accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
)

TaskRegistry.add(
    "ul2_lambada",
    source=seqio.TfdsDataSource(tfds_name="lambada:1.0.0",
                                splits={
                                    'validation': f'test[:32]',
                                }),
    preprocessors=[
        preprocessors.ul2_lambada,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.ul2_take_first_word,
    metric_fns=[metrics.accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES,
)



# ==================================HumanEval==================================



TaskRegistry.add(
    "humaneval",
    source=seqio.TfdsDataSource(tfds_name="human_eval:1.0.0",
                                splits={
                                    'validation': f'train',
                                }),
    preprocessors=[
        preprocessors.humaneval,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.ul2_humaneval,
    metric_fns=[metrics.accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
)


TaskRegistry.add(
    "ul2_humaneval",
    source=seqio.TfdsDataSource(tfds_name="human_eval:1.0.0",
                                splits={
                                    'validation': f'train',
                                }),
    preprocessors=[
        preprocessors.ul2_humaneval,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.ul2_humaneval,
    metric_fns=[metrics.accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES,
)


# ==================================bool_q==================================


TaskRegistry.add(
    "boolq",
    source=seqio.TfdsDataSource(tfds_name="bool_q:1.0.0",
                                splits={
                                    'validation': f'validation',
                                }),
    preprocessors=[
        preprocessors._process_boolq_v2,
        preprocessors.format_options,
        preprocessors.boolq,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.rank_classification,
    metric_fns=[metrics.ul2_boolq_accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES_V3,
)



TaskRegistry.add(
    "ul2_boolq",
    source=seqio.TfdsDataSource(tfds_name="bool_q:1.0.0",
                                splits={
                                    'validation': f'validation',
                                }),
    preprocessors=[
        preprocessors._process_boolq_v2,
        preprocessors.format_options,
        preprocessors.ul2_boolq,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.rank_classification,
    metric_fns=[metrics.ul2_boolq_accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES,
)


# ==================================ARC==================================


TaskRegistry.add(
    "arc",
    source=seqio.TfdsDataSource(
                                tfds_name="ai2_arc/ARC-Challenge:1.0.0", # tfds_name="ai2_arc/ARC-Easy:1.0.0", 
                                splits={
                                    'validation': f'test',
                                }),
    preprocessors=[
        preprocessors._process_arc,
        preprocessors._filter_arc,
        preprocessors.format_options_arc,
        preprocessors.arc,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.rank_classification,
    metric_fns=[metrics.ul2_arc_accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES_V2,
)

TaskRegistry.add(
    "ul2_arc",
    source=seqio.TfdsDataSource(
                                tfds_name="ai2_arc/ARC-Easy:1.0.0", # tfds_name="ai2_arc/ARC-Challenge:1.0.0",
                                splits={
                                    'validation': f'test[:32]',
                                }),
    preprocessors=[
        preprocessors._process_arc,
        preprocessors._filter_arc,
        preprocessors.format_options_arc,
        preprocessors.ul2_arc,
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        seqio.preprocessors.append_eos,
    ],
    postprocess_fn=postprocessors.rank_classification,
    metric_fns=[metrics.ul2_arc_accuracy],
    output_features=DEFAULT_OUTPUT_FEATURES,
)


# =============== PrefixLM objectives (not used in the T5 paper) ===============


# Vocabulary (shared by encoder and decoder)
sentencepiece_model_file = "gs://t5-data/vocabs/cc_all.32000.100extra/sentencepiece.model"

vocab = seqio.SentencePieceVocabulary(sentencepiece_model_file)

seqio.TaskRegistry.add(
    "c4_prefix_lm_objective_encoder_decoder_architecture",
    source=seqio.TfdsDataSource(tfds_name="c4/en:3.0.1"),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.targets_for_prefix_lm_objective,
        preprocessors.pack_prefix_lm_encoder_decoder,
    ],
    output_features={
        "encoder_input_tokens": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_target_tokens": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_input_tokens": seqio.Feature(vocabulary=vocab, add_eos=False),
        "encoder_segment_ids": seqio.Feature(vocabulary=vocab, add_eos=False),
        "encoder_positions": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_segment_ids": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_positions": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_loss_weights": seqio.Feature(vocabulary=vocab, add_eos=False),
        # All but the last stage of the preprocessing uses "targets" as the key,
        # so this output feature is necessary. It is not marked required because
        # the final preprocessor drops it.
        "targets": seqio.Feature(vocabulary=vocab, required=False),
    },
    metric_fns=[])


seqio.TaskRegistry.add(
    "c4_prefix_lm_objective_decoder_architecture",
    source=seqio.TfdsDataSource(tfds_name="c4/en:3.0.1"),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.targets_for_prefix_lm_objective,
        preprocessors.pack_prefix_lm_decoder_only,
    ],
    output_features={
        "decoder_target_tokens": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_input_tokens": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_loss_weights": seqio.Feature(vocabulary=vocab, add_eos=False),
        "decoder_causal_attention": seqio.Feature(
            vocabulary=vocab, add_eos=False),
        # All but the last stage of the preprocessing uses "targets" as the key,
        # so this output feature is necessary. It is not marked required because
        # the final preprocessor drops it.
        "targets": seqio.Feature(vocabulary=vocab, required=False),
    },
    metric_fns=[])


# UL2
TaskRegistry.add(
    "c4_v220_ul2_pack",
    source=seqio.TfdsDataSource(
        tfds_name="c4/en:3.0.1",
    ),
    preprocessors=[
        functools.partial(
            preprocessors.rekey, key_map={
                "inputs": None,
                "targets": "text"
            }),
        seqio.preprocessors.tokenize,
        seqio.CacheDatasetPlaceholder(),
        preprocessors.ul2_objective,
        seqio.preprocessors.append_eos_after_trim,
        preprocessors.pack_prefix_lm_decoder_only,
    ],
    output_features={
        "decoder_target_tokens": seqio.Feature(vocabulary=t5.data.get_default_vocabulary(), add_eos=False),
        "decoder_input_tokens": seqio.Feature(vocabulary=t5.data.get_default_vocabulary(), add_eos=False),
        "decoder_loss_weights": seqio.Feature(vocabulary=t5.data.get_default_vocabulary(), add_eos=False),
        "decoder_causal_attention": seqio.Feature(
            vocabulary=t5.data.get_default_vocabulary(), add_eos=False),
        "targets": seqio.Feature(vocabulary=t5.data.get_default_vocabulary(), required=False),
    },
    metric_fns=[])

