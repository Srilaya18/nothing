structure:
cicd-simple-java/
│── App.java
│── Dockerfile
│── Jenkinsfile
│── deployment.yaml
│── service.yaml




App.java:
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class App {

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        // Routes
        server.createContext("/results", new ResultsHandler());
        server.createContext("/events", new EventsHandler());
        server.createContext("/conference", new ConferenceHandler());
        server.createContext("/prices", new PricesHandler());
        server.createContext("/timetable", new TimetableHandler());

        server.setExecutor(null);
        server.start();

        System.out.println("Server started at http://localhost:8080");
    }

    // a. Student Results
    static class ResultsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = "{ \"name\":\"Harikrishna\", \"subjects\":[\"Math\",\"AI\",\"DBMS\"], \"marks\":[85,90,88] }";
            sendResponse(exchange, response);
        }
    }

    // b. Rivera Events
    static class EventsHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = "[\"Dance\",\"Music\",\"Coding\",\"Drama\",\"Sports\"]";
            sendResponse(exchange, response);
        }
    }

    // c. Conference Info
    static class ConferenceHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = "{ \"title\":\"AI Conference 2026\", \"venue\":\"VIT\", \"date\":\"May 2026\", \"speakers\":[\"Expert1\",\"Expert2\"] }";
            sendResponse(exchange, response);
        }
    }

    // d. Price List
    static class PricesHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = "{ \"Pen\":10, \"Notebook\":50, \"Bag\":500, \"Bottle\":30 }";
            sendResponse(exchange, response);
        }
    }

    // e. Timetable
    static class TimetableHandler implements HttpHandler {
        public void handle(HttpExchange exchange) throws IOException {
            String response = "{ \"Monday\":[\"Math\",\"AI\"], \"Tuesday\":[\"DBMS\",\"OS\"], \"Wednesday\":[\"CN\",\"ML\"], \"Thursday\":[\"SE\",\"AI Lab\"], \"Friday\":[\"Project\",\"Seminar\"] }";
            sendResponse(exchange, response);
        }
    }

    // Common Response Method
    static void sendResponse(HttpExchange exchange, String response) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(200, response.length());
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}




Dockerfile:
FROM openjdk:17

WORKDIR /app

COPY App.java .

RUN javac App.java

EXPOSE 8080

CMD ["java", "App"]





jenkinsfile:
pipeline {
    agent any

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/your-username/cicd-simple-java.git'
            }
        }

        stage('Build Java') {
            steps {
                sh 'javac App.java'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t simple-java-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8080:8080 simple-java-app'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
            }
        }
    }
}







deployment.yaml:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-java-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: simple-java
  template:
    metadata:
      labels:
        app: simple-java
    spec:
      containers:
      - name: simple-java-container
        image: simple-java-app
        ports:
        - containerPort: 8080






service.yaml:
apiVersion: v1
kind: Service
metadata:
  name: simple-java-service
spec:
  type: NodePort
  selector:
    app: simple-java
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30007







running how ani:
javac App.java
java App





test like what the output is:
http://localhost:8080/results
http://localhost:8080/events
http://localhost:8080/conference
http://localhost:8080/prices
http://localhost:8080/timetable