rule get_metadata:
    output:
        metadata=RESULTS / "metadata/{project}/{biosample}.tsv",
    log:
        LOGS / "get_metadata/{project}/{biosample}.log",
    threads: 1
    resources:
        time="5m",
        mem_mb=300,
    conda:
        ENVS / "metadata.yaml"
    params:
        url_stem="https://www.ebi.ac.uk/ena/browser/api/xml",
        timeout="60",
    script:
        SCRIPTS / "get_metadata.py"


rule combine_metadata:
    input:
        metadata=expand(
            str(RESULTS / "metadata/{project}/{biosample}.tsv"),
            project=[t[0] for t in project_samples],
            biosample=[t[1] for t in project_samples],
        ),
    output:
        sheet=RESULTS / "metadata/metadata.tsv"
    log:
        LOGS / "combine_metadata.log"
    threads: 8
    resources:
        time="1h",
        memory_mb=1000
    conda:
        ENVS / "metadata.yaml"
    script:
        SCRIPTS / "combine_metadata.py"
