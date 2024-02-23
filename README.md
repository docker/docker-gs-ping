# docker-gs-ping

This repo is forked from docker/docker-gs-ping and uses bitovi/github-actions-deploy-eks-helm@v1.2.9 to push the created container to eks via helm.

The helm charts can be found in the docker-gs-ping/actions-test folder which was created using helm create. 

to test the deployment:

➜  ~ curl http://eks.topsoilsystems.com
Hello, Docker! <3%
➜  ~ curl http://eks.topsoilsystems.com/health
{"Status":"OK"}

Terraform to create the eks cluster is here:
docker-gs-ping/eks_cluster


A simple Go server/microservice example for [Docker's Go Language Guide](https://docs.docker.com/language/golang/).

Notable features:

* Includes a [multi-stage `Dockerfile`](https://github.com/olliefr/docker-gs-ping/blob/main/Dockerfile.multistage).
* Has a CI pipeline using GitHub Actions to run tests.
* Has a CD pipeline using GitHub Actions to publish to Docker Hub.

## Want _moar_?!

There is a more advanced example in [olliefr/docker-gs-ping-roach](https://github.com/olliefr/docker-gs-ping-roach) using [CockroachDB](https://github.com/cockroachdb/cockroach).

## Contributing

This was written for an _introduction_ section of the Docker tutorial and as such it favours brevity and pedagogical clarity over robustness. 

Thus, feedback is welcome, but please no nits or pedantry. Ain't nobody got time for that 🙃

## License

[Apache-2.0 License](LICENSE)
