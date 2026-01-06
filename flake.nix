{
  description = "Environment Nix + Uv for SmartBrief";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python311
            uv
            zlib
            stdenv.cc.cc.lib
            glib
          ];

          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
            pkgs.glib
          ];

          shellHook = ''
            export UV_PYTHON_PREFERENCE="only-system"
          '';
        };
      }
    );
}
