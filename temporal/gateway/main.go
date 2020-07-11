package main

import (
	"context"
	"flag"
	"net/http"
	"fmt"
	"log"
  
	"github.com/grpc-ecosystem/grpc-gateway/runtime"
	"google.golang.org/grpc"
  
	gw "github.com/nick96/withoutdelay/temporal/gateway/gen/go" 
  )
  
  var (
	// command-line options:
	// gRPC server endpoint
	// port
	grpcServerEndpoint = flag.String("grpc-server-endpoint",  "localhost:9090", "gRPC server endpoint")
	port = flag.String("port", "8081", "port to expose the proxy on")
  )
  
  func run() error {
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)
	defer cancel()

	log.Printf("gRPC server endpoint: %s", grpcServerEndpoint)
	log.Printf("port: %s", port)
  
	// Register gRPC server endpoint
	// Note: Make sure the gRPC server is running properly and accessible
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithInsecure()}
	log.Printf("Proxying to gRPC server at %s", grpcServerEndpoint)
	err := gw.RegisterTemporalServiceHandlerFromEndpoint(ctx, mux,  *grpcServerEndpoint, opts)
	if err != nil {
	  return err
	}
  
	// Start HTTP server (and proxy calls to gRPC server endpoint)
	log.Printf("Running on port %s", port)
	return http.ListenAndServe(fmt.Sprintf(":%s", port), mux)
  }
  
  func main() {
	flag.Parse()
  
	if err := run(); err != nil {
	  log.Fatal(err)
	}
  }