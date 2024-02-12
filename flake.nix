{
  description = "ShiroBot, a Discord bot for my needs";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, poetry2nix, ... }:
    let pythonVer = "python311"; in
    {
      overlay = final: prev: {
    
        shirobot = final.poetry2nix.mkPoetryApplication {
          projectDir = self;
          preferWheels = true;
          python = final.${pythonVer};
        };

        shirobotEnv = final.poetry2nix.mkPoetryEnv {
          projectDir = self;
          preferWheels = true;
          python = final.${pythonVer};
          editablePackageSources = { shirobot = self; };
        };

        poetry = (prev.poetry.override { python = prev.${pythonVer}; });
      };
    } // (let

      forEachSystem = systems: func: nixpkgs.lib.genAttrs systems (system:
        func (import nixpkgs {
          inherit system;
          config.allowUnfree = true;
          overlays = [
            poetry2nix.overlay
            self.overlay
          ];
        })
      );

      forAllSystems = func: (forEachSystem [ "x86_64-linux" "aarch64-darwin" ] func);

    in {
      devShells = forAllSystems (pkgs: with pkgs; {
        default = mkShellNoCC {
          name = "shirobot";
          packages = [
            # this package            
            shirobotEnv

            # development dependencies
            poetry
          ];

          shellHook = ''
            export PYTHONPATH=${pkgs.${pythonVer}}
            export DISCORD_TOKEN="${builtins.readFile "/run/user/1000/secrets/shirobot_token"}"
          '';
        };
      });

      packages = forAllSystems (pkgs: {
        default = pkgs.shirobot;
        
        poetry = pkgs.poetry;
      });

    });
}
